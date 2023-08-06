#include <math.h>

#include "disptools.h"

 
/*! 
 * \brief Redistribute the volume change over the image. 
 *
 * Redistribute the change of volume within the body on the background,
 * and enforce the total volume change over the entire image to be zero.
 */ 
static inline void redistribute_volume_change( 
        const Image J, 
        const Mask mask 
        ) 
{ 
    FLOATING total_change = 0.0; 
    size_t background_voxels_count = 0; 
 
    for (size_t z = 0; z < J.nz; ++z) {
        for (size_t y = 0; y < J.ny; ++y) {
            for (size_t x = 0; x < J.nx; ++x) {
                total_change += __(J, x, y, z) - 1.0; 
                if (!__(mask, x, y, z)) { 
                    background_voxels_count += 1; 
                } 
            } 
        } 
    } 
 
    const FLOATING correction = -total_change / background_voxels_count; 
 
    for (size_t z = 0; z < J.nz; ++z) {
        for (size_t y = 0; y < J.ny; ++y) {
            for (size_t x = 0; x < J.nx; ++x) {
                if (!__(mask, x, y, z)) { 
                    __(J, x, y, z) = __(J, x, y, z) + correction; 
                } 
            } 
        } 
    } 
} 

/*!
 * \brief Compute a tolerance map over the volume.
 *
 * The tolerance is zero within the body volume and along the boundary,
 * while it is set to `tolerance' on the remaining background space.
 * Zero tolerance on the boundary prevents the vector field from 
 * flowing outside the image space in the contours of the regions
 * where the body touches the boundary.
 *
 * \note: The resulting `Image' object must be deallocated with `destroy_image'.
 */
static inline Image create_tolerance_map(
        const Mask mask,
        const FLOATING tolerance
        )
{
    const size_t nx = mask.nx, ny = mask.ny, nz = mask.nz;
    Image tolerance_map = new_image(1, nx, ny, nz, 1.0, 1.0, 1.0);

    if (!tolerance_map.data) {
        return tolerance_map;
    }

    for (size_t z = 0; z < nz; ++z) {
        for (size_t y = 0; y < ny; ++y) {
            for (size_t x = 0; x < nx; ++x) {
                if (__(mask, x, y, z) || 
                        x == 0    || y == 0    || z == 0 || 
                        x == nx-1 || y == ny-1 || z == nz-1) {
                    __(tolerance_map, x, y, z) = 0.0;
                }
                else {
                    __(tolerance_map, x, y, z) = tolerance;
                }
            }
        }
    }
    return tolerance_map;
}

/*!
 * \brief Compute the error on the Jacobian of the moving field.
 */
static inline FLOATING compute_error(
        const Image J,            /*!< Target Jacobian */
        const Image J_field,      /*!< Current Jacobian */
        const Mask mask,          /*!< Body mask */
        const FLOATING tolerance, /*!< Jacobian tolerance on background */
        const Image voxel_error,  /*!< Error on the Jacobian */
        FLOATING *max_voxel_error /*!< Maximum voxel error */
        )
{
    // Cumulative error over the entire Jacobian map
    FLOATING total_error = 0.0;

    // Local variable for maximum voxel error
    FLOATING max_error = 0.0;

    // Compute the error on the Jacobian map for all voxels
#ifdef __GNUC__
    #define MAX_ERROR_ACC max_error
    #pragma omp parallel for \
            reduction(+: total_error) \
            reduction(max: max_error) \
            collapse(3) \
            schedule(static)
    for (size_t z = 0; z < J.nz; ++z) {
        for (size_t y = 0; y < J.ny; ++y) {
            for (size_t x = 0; x < J.nx; ++x) {

#else // MSVC 15 does not support OpenMP > 2.0
    #define MAX_ERROR_ACC local_max_error
    #pragma omp parallel
    {

    FLOATING local_max_error = 0.0;

    int z;
    #pragma omp for nowait \
            reduction(+: total_error)
    for (z = 0; z < J.nz; ++z) {
        for (size_t y = 0; y < J.ny; ++y) {
            for (size_t x = 0; x < J.nx; ++x) {
#endif
                // Compute the error on the voxel
                FLOATING error = __(J_field, x, y, z) - __(J, x, y, z);

                // Inside the body mask
                if (__(mask, x, y, z)) {
                    __(voxel_error, x, y, z) = error;
                }
                // Tolerate some error in the background
                else {
                    const FLOATING abs_error = fabs(error);
                    __(voxel_error, x, y, z) = 
                        abs_error < tolerance ? 
                        0.0 :
                        copysign(abs_error - tolerance, error);
                }

                // Update total and maximum local errors
                // The maximum voxel error is checked only within the
                // body volume marked by the mask 
                total_error += __(voxel_error, x, y, z) * __(voxel_error, x, y, z);
                if (__(mask, x, y, z) && fabs(__(voxel_error, x, y, z)) > MAX_ERROR_ACC) {
                    MAX_ERROR_ACC = fabs(__(voxel_error, x, y, z));
                }
            }
        }
    }

#ifndef __GNUC__
    // Manual max reduction, MSVC 15 does not provide it
    #pragma omp critical
    {
        if (local_max_error > max_error) {
            max_error = local_max_error;
        }
    }

    } // pragma omp parallel
#endif
    #undef MAX_ERROR_ACC

    // Return maximum voxel error
    *max_voxel_error = max_error;

    return total_error;
}

