import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
from findiff.findiff import FinDiff, Coef, Identity


class FinDiffTest(unittest.TestCase):

    def test_partial_diff(self):
        nx = 100
        x = np.linspace(0, np.pi, nx)
        u = np.sin(x)
        ux_ex = np.cos(x)

        fd = FinDiff(0, x[1] - x[0], 1)
        fd.acc = 4

        ux = fd(u)

        assert_array_almost_equal(ux, ux_ex, decimal=5)

        ny = 100
        y = np.linspace(0, np.pi, ny)
        X, Y = np.meshgrid(x, y, indexing='ij')

        u = np.sin(X) * np.sin(Y)
        uxy_ex = np.cos(X) * np.cos(Y)

        fd = FinDiff((0, x[1] - x[0], 1), (1, y[1] - y[0], 1))
        fd.acc = 4

        uxy = fd(u)

        assert_array_almost_equal(uxy, uxy_ex, decimal=5)

    def test_plus(self):

        (X, Y), _, h = grid(2, 50, 0, 1)

        u = X**2 + Y**2
        d_dx = FinDiff(0, h[0])
        d_dy = FinDiff(1, h[1])

        d = d_dx + d_dy

        u1 = d(u)
        u1_ex = 2*X + 2*Y

        assert_array_almost_equal(u1, u1_ex)

    def test_multiply(self):

        (X, Y), _, h = grid(2, 5, 0, 1)

        u = X**2 + Y**2
        d2_dx2 = FinDiff(0, h[0], 2)

        d = Coef(X) * d2_dx2

        u1 = d(u)
        assert_array_almost_equal(u1, 2*X)

    def test_multiply_operators(self):

        (X, Y), _, h = grid(2, 50, 0, 1)

        u = X**2 + Y**2
        d_dx = FinDiff(0, h[0])

        d2_dx2_test = d_dx * d_dx

        uxx = d2_dx2_test(u)

        assert_array_almost_equal(uxx, np.ones_like(X)*2)

    def test_laplace(self):

        (X, Y, Z), _, h = grid(3, 50, 0, 1)

        u = X**3 + Y**3 + Z**3

        d2_dx2, d2_dy2, d2_dz2 = [FinDiff(i, h[i], 2) for i in range(3)]

        laplace = d2_dx2 + d2_dy2 + d2_dz2

        lap_u = laplace(u)
        assert_array_almost_equal(lap_u, 6*X + 6*Y + 6*Z)

        d_dx, d_dy, d_dz = [FinDiff(i, h[i]) for i in range(3)]

        d = Coef(X) * d_dx + Coef(Y) * d_dy + Coef(Z) * d_dz

        f = d(lap_u)

        d2 = d * laplace
        f2 = d2(u)

        assert_array_almost_equal(f2, f)
        assert_array_almost_equal(f2, 6 * (X + Y + Z))

    def test_non_uniform_3d(self):
        x = np.r_[np.arange(0, 4, 0.05), np.arange(4, 10, 1)]
        y = np.r_[np.arange(0, 4, 0.05), np.arange(4, 10, 1)]
        z = np.r_[np.arange(0, 4.5, 0.05), np.arange(4.5, 10, 1)]
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        f = np.exp(-X**2-Y**2-Z**2)

        d_dy = FinDiff(1, y, acc=4)
        fy = d_dy(f)
        fye = - 2 * Y * np.exp(-X**2-Y**2-Z**2)
        assert_array_almost_equal(fy, fye, decimal=4)

    def test_FinDiff_NonUni_2d(self):
        x = np.r_[np.arange(0, 4, 0.005), np.arange(4, 10, 1)]
        y = np.r_[np.arange(0, 4, 0.005), np.arange(4, 10, 1)]
        X, Y = np.meshgrid(x, y, indexing='ij')
        f = np.exp(-X**2-Y**2)

        d_dx = FinDiff((0, x, 1))
        fx = d_dx(f)
        fxe = - 2 * X * np.exp(-X**2-Y**2)
        assert_array_almost_equal(fx, fxe, decimal=4)

    def test_BasicFinDiffNonUni_3d(self):
        x = np.r_[np.arange(0, 4, 0.05), np.arange(4, 10, 1)]
        y = np.r_[np.arange(0, 4, 0.05), np.arange(4, 10, 1)]
        z = np.r_[np.arange(0, 4.5, 0.05), np.arange(4.5, 10, 1)]
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        f = np.exp(-X**2-Y**2-Z**2)

        d_dy = FinDiff(1, y, acc=4)
        fy = d_dy(f)
        fye = - 2 * Y * np.exp(-X**2-Y**2-Z**2)
        assert_array_almost_equal(fy, fye, decimal=4)

    def test_identity(self):

        x = np.linspace(-1, 1, 100)
        u = x**2
        identity = Identity()

        assert_array_equal(u, identity(u))

        twice_id = Coef(2) * Identity()
        assert_array_equal(2 * u, twice_id(u))

        x_id = Coef(x) * Identity()
        assert_array_equal(x * u, x_id(u))

    def test_identity_2d(self):

        (X, Y), (x, y), _ = grid(2, 100, -1, 1)

        u = X ** 2 + Y ** 2
        identity = Identity()

        assert_array_equal(u, identity(u))

        twice_id = Coef(2) * Identity()
        assert_array_equal(2 * u, twice_id(u))

        x_id = Coef(X) * Identity()
        assert_array_equal(X * u, x_id(u))

        dx = x[1] - x[0]
        d_dx = FinDiff(0, dx)
        linop = d_dx + 2 * Identity()
        assert_array_almost_equal(2 * X + 2*u, linop(u))

    def test_spac(self):

        (X, Y), _, (dx, dy) = grid(2, 100, -1, 1)

        u = X**2 + Y**2

        d_dx = FinDiff(0, dx)
        d_dy = FinDiff(1, dy)

        assert_array_almost_equal(2*X, d_dx(u))
        assert_array_almost_equal(2*Y, d_dy(u))

        d_dx = FinDiff(0, dx)
        d_dy = FinDiff(1, dy)

        u = X*Y
        d2_dxdy = d_dx * d_dy

        assert_array_almost_equal(np.ones_like(u), d2_dxdy(u))

    def test_mixed_partials(self):

        (X, Y, Z), _, (dx, dy, dz) = grid(3, 50, 0, 1)

        u = X**2 * Y**2 * Z**2

        d3_dxdydz = FinDiff((0, dx), (1, dy), (2, dz))
        diffed = d3_dxdydz(u)
        assert_array_almost_equal(8*X*Y*Z, diffed)


def grid(ndim, npts, a, b):

    if not hasattr(a, "__len__"):
        a = [a] * ndim
    if not hasattr(b, "__len__"):
        b = [b] * ndim
    if not hasattr(np, "__len__"):
        npts = [npts] * ndim

    coords = [np.linspace(a[i], b[i], npts[i]) for i in range(ndim)]
    mesh = np.meshgrid(*coords, indexing='ij')
    spac = [coords[i][1] - coords[i][0] for i in range(ndim)]

    return mesh, coords, spac

if __name__ == '__main__':
    unittest.main()