import numpy as np
from scipy.constants import c, pi

from algorithms.pdf_integrators_2d import dblquad


class RfBucket():

    def __init__(self) -> None:
        self.C = 1
        self.gamma_tr = 1

        self._V = None
        self._h = None
        self._phi = None
        self._phi_s = None

        self._p0 = None
        self._gamma = None
        self._beta = None
        self._mass = None

        self._eta = None

    @property
    def p0(self):
        return

    @p0.setter
    def p0(self, value):
        pass

    @property
    def beta(self):
        return

    @beta.setter
    def beta(self, value):
        pass

    @property
    def gamma(self):
        return

    @gamma.setter
    def gamma(self, value):
        pass

    @property
    def eta(self):
        return

    @eta.setter
    def eta(self, value):
        pass

    def g(self, V, p0, phis):
        def H(phi, delta):
            return (
                    -1. / 2 * self.eta * self.beta * c * delta ** 2 +
                    c * V / (2 * pi * self.p0 * self.h) * (
                                np.cos(phi) - np.cos(self.phis) + (phi - self.phis) * np.sin(self.phis))
            )

        return H

    def f(self, V, p0, phis):
        gamma = np.sqrt(1 + (p0 / self.mass) ** 2)
        beta = np.sqrt(1 - 1 / gamma ** 2)
        eta = -gamma ** -2 + self.gamma_tr ** -2

        def dp(phi):
            A = c * V * (phi * np.sin(phis) - pi * np.sin(phis) + np.cos(phi) + 1) / (pi * beta * c * eta * self.h * p0)
            A = A.clip(min=0)
            return np.sqrt(A)

        #         if A < 0:
        #             return 0
        #         else:
        #             return np.sqrt(A)
        return dp

    def emittance(self, f, x0, x1, p0=p0):
        conv = 2 * pi * self.h / self.C
        Q, error = dblquad(lambda y, x: 1, x0, x1,
                           lambda x: 0, f)

        return Q * 2 * self.p0 / c * 1 / conv
