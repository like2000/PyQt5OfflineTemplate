import time

import numpy as np
from scipy.constants import c, e, m_p, pi

from algorithms.pdf_integrators_2d import dblquad


class RfBucket():

    def __init__(self, C=1, gamma_tr=1, p0=1, h=1) -> None:
        """Mass is in eV; p0 is in eV/c"""
        self.mass = m_p * c ** 2 / e # in eV

        self.C = C
        self.p0 = p0
        self.gamma_tr = gamma_tr

        self.V = 1
        self.h = h
        self.phi = 0
        self.phi_s = 0

    @property
    def p0(self):
        """p0 in eV/c"""
        return self._p0

    @p0.setter
    def p0(self, value):
        self._gamma = np.sqrt(1 + (value / self.mass) ** 2)
        self._beta = np.sqrt(1 - self.gamma**-2)
        self._p0 = value

    @property
    def beta(self):
        return self._beta

    @property
    def gamma(self):
        return self._gamma

    @property
    def eta(self):
        return self.gamma_tr**-2 - self.gamma**-2

    @eta.setter
    def eta(self, value):
        self._eta = value

    def H(self, phi, delta, normalized=True):
        if normalized:
            conv = 2 * pi * self.h / self.C
            norm = self.p0 / c * 1 / conv
        else:
            norm = 1

        H = (
            -1/2 * self.eta * self.beta * c * delta ** 2 * 1/norm +
            c * self.V / (2 * pi * self.p0 * self.h) * (
                np.cos(phi) - np.cos(self.phi_s) + (phi - self.phi_s) * np.sin(self.phi_s)) * norm
        )

        return H

    def dp(self, phi, normalized=True):
        if normalized:
            conv = 2 * pi * self.h / self.C
            norm = self.p0 / c * 1 / conv
        else:
            norm = 1

        A = c * self.V * (phi * np.sin(self.phi_s) - pi * np.sin(self.phi_s) + np.cos(phi) + 1) / \
            (pi * self.beta * c * self.eta * self.h * self.p0)
        A = A.clip(min=0)

        return np.sqrt(A) * norm

    def emittance(self, f, x0, x1, normalized=False):
        conv = 2 * pi * self.h / self.C
        Q, error = dblquad(lambda y, x: 1, x0, x1,
                           lambda x: 0, f)

        if normalized:
            return Q * 2 * self.p0 / c * 1 / conv
        else:
            return Q * 2

    def bucket_area(self):

        return self.emittance(self.dp, -pi, pi)

    def update_bucket_params(self, V, phi_s, p0):

        self.phi_s = phi_s
        self.p0 = p0
        self.V = V

    def bucket_area_function(self, V, phi_s, p0):
        V0, phi_s0, p00 = self.V, self.phi_s, self.p0
        area = []

        t0 = time.clock()
        for (Vi, phi_si, p0i) in zip(V, phi_s, p0):
            self.update_bucket_params(Vi, phi_si, p0i)
            area.append(self.bucket_area())

        print(f"Time elapsed: {time.clock() - t0}")
        self.V, self.phi_s, self.p0 = V0, phi_s0, p00

        return np.array(area)
