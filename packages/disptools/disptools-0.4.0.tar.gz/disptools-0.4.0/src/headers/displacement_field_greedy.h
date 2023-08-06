#ifndef __DISPLACEMENT_FIELD_GREEDY_DEFINED
#define __DISPLACEMENT_FIELD_GREEDY_DEFINED

#include "disptools.h"
#include <stdbool.h>

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
        );

#endif // __DISPLACEMENT_FIELD_GREEDY_DEFINED
