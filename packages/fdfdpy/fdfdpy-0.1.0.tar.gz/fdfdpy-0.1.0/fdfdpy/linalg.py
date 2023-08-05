import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'pyMKL')))

from fdfdpy.constants import DEFAULT_MATRIX_FORMAT, DEFAULT_SOLVER
from fdfdpy.constants import EPSILON_0, MU_0
from fdfdpy.pml import S_create
from fdfdpy.derivatives import createDws

from pyMKL import pardisoSolver
from scipy.sparse import spdiags, eye
from scipy.sparse.linalg import spsolve, eigs
from scipy.sparse import hstack as sp_hstack
from scipy.sparse import vstack as sp_vstack
from time import time
from numpy import complex128, array, asarray, roll, diff, prod, zeros, real, imag, float64, hstack


def grid_average(center_array, w):
    # computes values at cell edges

    xy = {'x': 0, 'y': 1}
    center_shifted = roll(center_array, 1, axis=xy[w])
    avg_array = (center_shifted+center_array)/2
    return avg_array


def dL(N, xrange, yrange=None):
    # solves for the grid spacing

    if yrange is None:
        L = array([diff(xrange)[0]])  # Simulation domain lengths
    else:
        L = array([diff(xrange)[0],
                   diff(yrange)[0]])  # Simulation domain lengths
    return L/N


def is_equal(matrix1, matrix2):
    # checks if two sparse matrices are equal

    return (matrix1!=matrix2).nnz==0


def construct_A(omega, xrange, yrange, eps_r, NPML, pol, L0,
                averaging=True,
                timing=False,
                matrix_format=DEFAULT_MATRIX_FORMAT):
    # makes the A matrix
    N = asarray(eps_r.shape)  # Number of mesh cells
    M = prod(N)  # Number of unknowns

    EPSILON_0_ = EPSILON_0*L0
    MU_0_ = MU_0*L0

    if pol == 'Ez':
        vector_eps_z = EPSILON_0_*eps_r.reshape((-1,))
        T_eps_z = spdiags(vector_eps_z, 0, M, M, format=matrix_format)

        (Sxf, Sxb, Syf, Syb) = S_create(omega, L0, N, NPML, xrange, yrange, matrix_format=matrix_format)

        # Construct derivate matrices
        Dyb = Syb.dot(createDws('y', 'b', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dxb = Sxb.dot(createDws('x', 'b', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dxf = Sxf.dot(createDws('x', 'f', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dyf = Syf.dot(createDws('y', 'f', dL(N, xrange, yrange), N, matrix_format=matrix_format))

        A = (Dxf*1/MU_0_).dot(Dxb) \
            + (Dyf*1/MU_0_).dot(Dyb) \
            + omega**2*T_eps_z
        # A = A / (omega**2*EPSILON_0)        # normalize A to be unitless.  (note, this isn't in original fdfdpy)

    elif pol == 'Hz':
        if averaging:
            vector_eps_x = grid_average(EPSILON_0_*eps_r, 'x').reshape((-1,))
            vector_eps_y = grid_average(EPSILON_0_*eps_r, 'y').reshape((-1,))
        else:
            vector_eps_x = EPSILON_0_*eps_r.reshape((-1,))
            vector_eps_y = EPSILON_0_*eps_r.reshape((-1,))

        # Setup the T_eps_x, T_eps_y, T_eps_x_inv, and T_eps_y_inv matrices
        T_eps_x = spdiags(vector_eps_x, 0, M, M, format=matrix_format)
        T_eps_y = spdiags(vector_eps_y, 0, M, M, format=matrix_format)
        T_eps_x_inv = spdiags(1/vector_eps_x, 0, M, M, format=matrix_format)
        T_eps_y_inv = spdiags(1/vector_eps_y, 0, M, M, format=matrix_format)

        (Sxf, Sxb, Syf, Syb) = S_create(omega, L0, N, NPML, xrange, yrange, matrix_format=matrix_format)

        # Construct derivate matrices
        Dyb = Syb.dot(createDws('y', 'b', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dxb = Sxb.dot(createDws('x', 'b', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dxf = Sxf.dot(createDws('x', 'f', dL(N, xrange, yrange), N, matrix_format=matrix_format))
        Dyf = Syf.dot(createDws('y', 'f', dL(N, xrange, yrange), N, matrix_format=matrix_format))

        A = Dxf.dot(T_eps_x_inv).dot(Dxb) \
            + Dyf.dot(T_eps_y_inv).dot(Dyb) \
            + omega**2*MU_0_*eye(M)

        # A = A / (omega**2*MU_0)     # normalize A to be unitless.  (note, this isn't in original fdfdpy)

    else:
        raise ValueError("something went wrong and pol is not one of Ez, Hz, instead was given {}".format(pol))

    derivs = {
        'Dyb' : Dyb,
        'Dxb' : Dxb,
        'Dxf' : Dxf,
        'Dyf' : Dyf
    }

    return (A, derivs)


def solver_eigs(A, Neigs, guess_value=0, guess_vector=None, timing=False):
    # solves for the eigenmodes of A

    if timing:
        start = time()
    (values, vectors) = eigs(A, k=Neigs, sigma=guess_value, v0=guess_vector, which='LM')
    if timing:
        end = time()
        print('Elapsed time for eigs() is %.4f secs' % (end - start))
    return (values, vectors)


def solver_direct(A, b, timing=False, solver=DEFAULT_SOLVER):
    # solves linear system of equations

    b = b.astype(complex128)
    b = b.reshape((-1,))

    if not b.any():
        return zeros(b.shape)

    if timing:
        t = time()

    if solver.lower() == 'pardiso':
        pSolve = pardisoSolver(A, mtype=13) # Matrix is complex unsymmetric due to SC-PML
        pSolve.factor()
        x = pSolve.solve(b)
        pSolve.clear()

    elif solver.lower() == 'scipy':
        x = spsolve(A, b)

    else:
        raise ValueError('Invalid solver choice: {}, options are pardiso or scipy'.format(str(solver)))

    if timing:
        print('Linear system solve took {:.2f} seconds'.format(time()-t))

    return x

def solver_complex2real(A11, A12, b, timing=False, solver=DEFAULT_SOLVER):
    # solves linear system of equations [A11, A12; A21*, A22*]*[x; x*] = [b; b*]

    b = b.astype(complex128)
    b = b.reshape((-1,))
    N = b.size

    if not b.any():
        return zeros(b.shape)

    b_re = real(b).astype(float64)
    b_im = imag(b).astype(float64)

    Areal = sp_vstack((sp_hstack((real(A11) + real(A12), -imag(A11) + imag(A12))), \
            sp_hstack((imag(A11) + imag(A12), real(A11) - real(A12)))))

    if timing:
        t = time()

    if solver.lower() == 'pardiso':
        pSolve = pardisoSolver(Areal, mtype=11) # Matrix is real unsymmetric
        pSolve.factor()
        x = pSolve.solve(hstack((b_re, b_im)))
        pSolve.clear()

    elif solver.lower() == 'scipy':
        x = spsolve(Areal, hstack((b_re, b_im)))

    else:
        raise ValueError('Invalid solver choice: {}, options are pardiso or scipy'.format(str(solver)))

    if timing:
        print('Linear system solve took {:.2f} seconds'.format(time()-t))

    return (x[:N] + 1j*x[N:2*N])
