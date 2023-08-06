#include <assert.h>
#include <math.h>
#include <stdlib.h>
#include <float.h>
#include <string.h>
#include <stdbool.h>

#include "disptools.h"
#include "displacement_field_greedy.h"
#include "jacobian.h"
#include "error.h"

/*!
 * \brief Update the displacement field according to the error
 *        on the Jacobian map.
 *
 * Each component of the displacement field is updated independently.
 * For each component, check the error on the two neighbours. If the
 * error is positive (negative) on the preceding (following) voxel
 * along the direction, then the value of the field must be decreased,
 * vice versa for errors of the opposite sign.
 */
static inline void greedy_step(
        const Image old_field,     /*!< Current displacement field */
        const Image new_field,     /*!< New displacement field */
        const Image voxel_error,   /*!< Error on the Jacobian */
        const FLOATING eta      /*!< Step length parameter */
        )
{
    // Do not iterate over the voxels on the boundary
    const size_t x_max = old_field.nx - 1;
    const size_t y_max = old_field.ny - 1;
    const size_t z_max = old_field.nz - 1;

    // Precompute fractional step for each direction
    const FLOATING ddx = eta * old_field.dx * .5f;
    const FLOATING ddy = eta * old_field.dy * .5f;
    const FLOATING ddz = eta * old_field.dz * .5f;

    // Update the displacement vectors in each voxel according to the error
#ifdef __GNUC__
    #pragma omp parallel for collapse(3) schedule(static)
    for (size_t z = 1; z < z_max; ++z) {
        for (size_t y = 1; y < y_max; ++y) {
            for (size_t x = 1; x < x_max; ++x) {
#else // MSVC 15 does not support OpenMP > 2.0
    int z;
    #pragma omp parallel for
    for (z = 1; z < z_max; ++z) {
        for (size_t y = 1; y < y_max; ++y) {
            for (size_t x = 1; x < x_max; ++x) {
#endif

                const FLOATING delta_x = ddx * (__(voxel_error, x+1, y,   z  ) -
                                                __(voxel_error, x-1, y,   z  ));
                const FLOATING delta_y = ddy * (__(voxel_error, x,   y+1, z  ) -
                                                __(voxel_error, x,   y-1, z  ));
                const FLOATING delta_z = ddz * (__(voxel_error, x,   y,   z+1) -
                                                __(voxel_error, x,   y,   z-1));

                _(new_field, x, y, z, X) = _(old_field, x, y, z, X) + delta_x;
                _(new_field, x, y, z, Y) = _(old_field, x, y, z, Y) + delta_y;
                _(new_field, x, y, z, Z) = _(old_field, x, y, z, Z) + delta_z;
            }
        }
    }
}

/*!
 * \brief Find a displacement field that realises the given Jacobian.
 *
 * Employ a greedy search, starting from an initial guess of the
 * displacement field (passed in the `field' argument). At each
 * iteration, compute the Jacobian of the current displacement field,
 * then correct the components of the field on each voxel according to
 * the error on the neighbours. Each component is corrected
 * independently, according to the two neighbours along that direction.
 *
 * Use two couples of buffers, to store a copy of the displacement field
 * and its Jacobian at the current iteration, before and after the
 * correction. If the correction improves the result, then switch the
 * buffers and proceed with the next iteration, otherwise keep the
 * current displacement field.
 */
void generate_displacement_greedy(
        const size_t nx,          /*!< Width of the image  */
        const size_t ny,          /*!< Length of the image */
        const size_t nz,          /*!< Depth of the image  */
        const FLOATING dx,        /*!< x spacing */
        const FLOATING dy,        /*!< y spacing */
        const FLOATING dz,        /*!< z spacing */
        const FLOATING *J,        /*!< Target Jacobian */
        const bool *mask,         /*!< Body mask */
        const FLOATING epsilon,   /*!< Tolerance on the Jacobian per voxel */
        const FLOATING tolerance, /*!< Jacobian tolerance on background */
        FLOATING eta,             /*!< Initial step length for the optimisation */
        const FLOATING eta_max,   /*!< Maximum step length allowed */
        const FLOATING alpha,     /*!< Step length increase coefficient */
        const FLOATING beta,      /*!< Step length decrease coefficient */
        const FLOATING gamma,     /*!< Armijo-Goldstein parameter */
        const FLOATING delta,     /*!< Jacobian regularisation threshold */
        const FLOATING zeta,      /*!< Jacobian regularisation weight */
        const FLOATING theta,     /*!< Termination condition based on improvement */
        const FLOATING iota,      /*!< Termination condition based on eta */
        const bool strict,        /*!< Always improve maximum voxel error */
        const size_t it_max,      /*!< Maximum number of iterations */
        FLOATING *field           /*!< Resulting displacement field */
        )
{
    ASSERT_PARAMETERS;
    disptools_clear_error();

    // Image size
    const size_t voxel_number = nx * ny * nz;
    const size_t image_size = voxel_number * sizeof (FLOATING);

    // Use two buffers that are swapped
    unsigned old_buffer = 0, new_buffer = 1;

    // Wrap arrays in data strucutres
    Image J_ = {1, nx, ny, nz, dx, dy, dz, (FLOATING*) J};
    Mask mask_ = {nx, ny, nz, (bool*) mask};

    // Allocate memory for the Jacobian map of the moving field
    // Use two buffers
    Image J_field_[2] = {
        new_image(3, nx, ny, nz, dx, dy, dz),
        new_image(3, nx, ny, nz, dx, dy, dz),
    };

    // Allocate memory for the moving field
    // Use two buffers
    Image field_[2] = {
        new_image(3, nx, ny, nz, dx, dy, dz),
        new_image(3, nx, ny, nz, dx, dy, dz),
    };

    // Allocate memory for the voxel error term
    Image voxel_error = new_image(1, nx, ny, nz, dx, dy, dz);

    FLOATING last_error = DBL_MAX, error = DBL_MAX;
    FLOATING max_voxel_error = 0.0;

    if (disptools_has_error()) {
        goto cleanup;
    }

    // Copy initial guess in the buffer
    memcpy(field_[old_buffer].data, field, 3 * image_size);

    // Compute the error of the initial guess
    jacobian(field_[old_buffer], J_field_[old_buffer]);
    last_error = compute_error(J_,
                               J_field_[old_buffer],
                               mask_,
                               tolerance,
                               voxel_error,
                               &max_voxel_error
                               );

    size_t it;
    for (it = 1; it <= it_max; ++it) {

        // Update the moving displacement field
        greedy_step(field_[old_buffer],
                    field_[new_buffer],
                    voxel_error,
                    eta
                    );

        // Compute the Jacobian map of the moving displacement field
        jacobian(field_[new_buffer], J_field_[new_buffer]);

        // Compute the error of the moving field
        error = compute_error(J_,
                              J_field_[new_buffer],
                              mask_,
                              tolerance,
                              voxel_error,
                              &max_voxel_error
                              );

        // Verbose feedback
        verbose_printf(true,
                       "Iteration %5ld:  "
                       "total error %6e  "
                       "max voxel error %6e  "
                       "eta %6e\n",
                       it, error, max_voxel_error, eta);

        // Stopping conditions

        if (!isnormal(error)) {
            verbose_printf(true, "Terminating: error exploded.\n");
            break;
        }

        if (error >= last_error) {
            // Try to reduce the step size
            eta *= beta;

            // Terminate if eta is too small
            if (eta < iota) {
                verbose_printf(true, "Error not decreasing, terminating.\n");
                break;
            }

            // Otherwise, repeat the last iteration with the new eta
            --it;
            verbose_printf(true, "Error not decreasing, "
                                 "reducing step size to %.4e\n", eta);
            continue;
        }

        if (1.0 - error / last_error < theta) {
            verbose_printf(true, "Error not decreasing, terminating.\n");
            break;
        }

        if (!isnormal(max_voxel_error)) {
            verbose_printf(true, "Terminating: voxel error exploded.\n");
            break;
        }

        if (max_voxel_error < epsilon) {
            verbose_printf(true, "Terminating: reached desired tolerance.\n");
            break;
        }

        // Save error and swap the buffers
        last_error = error;
        XOR_SWAP(old_buffer, new_buffer);
    }

    verbose_printf(it == it_max, "Terminating: reached maximum number of iterations.\n");

    // Copy result for the caller
    memcpy(field, field_[old_buffer].data, 3 * image_size);

cleanup:
    // Release buffers
    delete_image(&field_[0]);
    delete_image(&field_[1]);
    delete_image(&J_field_[0]);
    delete_image(&J_field_[1]);
    delete_image(&voxel_error);
}
