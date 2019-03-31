import numpy as np
from scipy.constants import c, e, m_p, pi
from scipy.integrate import cumtrapz, dblquad
from scipy.optimize import brentq


class RfBucket():

    def __init__(self, momentum, bdot, voltage, eta, ratio):

        # Constants
        # =========
        self.h = 4620.
        self.C = 6911.
        self.mass = m_p * c ** 2 / e
        self.conv = 2 * pi * self.h / self.C

        # Function values
        # ===============
        self.momentum = momentum
        self.bdot = bdot
        self.voltage = voltage
        self.eta = eta
        self.ratio = ratio

        self.update_parameters(1400)

    #         # Force - to find roots - this perhaps needs to be moved actually!
    #         # Could be a bug in the original implementation...
    #         # =====================
    #         ff = np.linspace(-1.*pi, 1.1*pi, 100)
    #         F = lambda phi: (np.sin(phi) - np.sin(self.phi_s)) + 4*self.r0*(np.sin(4*(phi-self.phi_s)))
    #         fc = get_roots(F, ff)
    #         ix = np.argsort(np.abs(fc - self.phi_s))
    #         print(fc)

    #         fc = fc[ix]
    #         self.sfp, self.ufp = fc[0::2], fc[1::2]
    #         self.phi_c = self.ufp[0]
    #         print(self.phi_c)

    def update_parameters(self, time):
        self.p0 = self.momentum(time)
        self.gamma = np.sqrt(1 + (self.p0 / self.mass) ** 2)
        self.beta = np.sqrt(1 - 1. / self.gamma ** 2)
        self.eta0 = self.eta(time)
        self.V0 = self.voltage(time)
        if isinstance(self.ratio, float):
            self.r0 = self.ratio
        else:
            self.r0 = self.ratio(time)
        self.phi_s = np.arcsin(self.bdot(time) * 6911 * 741. / self.V0)
        #         self.phi_s = np.arcsin(self.bdot(time) * 6911 * 900. / self.V0)

        # Force - to find roots
        # =====================
        ff = np.linspace(-1. * pi, 1.1 * pi, 100)
        fc = self._get_roots(self.F, ff)
        ix = np.argsort(np.abs(fc - self.phi_s))

        fc = fc[ix]
        # TODO: handle sign of eta in here
        self.sfp, self.ufp = fc[0::2], fc[1::2]
        try:
            self.phi_c = self.ufp[0]
        except IndexError:
            self.phi_c = 0

        return self

    # Helper functions - voltage and force
    # ====================================
    def V(self, phi):
        res = c * self.V0 / (2 * pi * self.p0 * self.h) * (
                np.cos(phi) - np.cos(self.phi_s) + (phi - self.phi_s) * np.sin(self.phi_s)
                + self.r0 * np.cos(4 * (phi - self.phi_s)))

        return res

    def F(self, phi):
        res = (np.sin(phi) - np.sin(self.phi_s)) + 4 * self.r0 * (np.sin(4 * (phi - self.phi_s)))

        return res

    # Actual dp curve
    # ===============
    def dp(self, phi):
        res = 2. / (self.eta0 * self.beta * c) * (self.V(phi) - self.V(self.phi_c)).clip(min=0)
        res = np.sqrt(res)

        return res

    def hamiltonian(self, delta, phi):
        res = (-1 / 2. * self.eta0 * self.beta * c * delta ** 2 + self.V(phi) - self.V(self.phi_c))

        return res

    def H(self, phi, delta):
        return self.hamiltonian(delta, phi)

    # Emittance
    # =========
    def get_emittance(self, method='trapz'):

        if method == 'trapz':
            res = self._emittance_trapz(self.dp, -pi, self.phi_c, p0=self.p0)
        else:
            raise RuntimeError("Bad method!")

        return res

    # Convenience functions
    # =====================
    def _get_roots(self, f, x):
        y = f(x)
        ix = np.where(np.abs(np.diff(np.sign(y))) == 2)[0]
        x0 = np.array([brentq(f, x[i], x[i + 1]) for i in ix])

        return x0

    def _quad2d(self, f, ylimits, xmin, xmax):
        Q, error = dblquad(lambda y, x: f(x, y), xmin, xmax,
                           lambda x: -ylimits(x), lambda x: ylimits(x))

        return Q

    def _emittance(self, f, x0, x1, p0):
        Q, error = dblquad(lambda y, x: 1, x0, x1,
                           lambda x: 0, f)

        return Q * 2 * p0 / c * 1 / self.conv;

    def _emittance_trapz(self, f, x0, x1, p0):
        x = np.linspace(x0, x1, 100)
        y = f(x)
        Q = np.trapz(y, x)

        return Q * 2 * p0 / c * 1 / self.conv;

    def _emittance_cumtrapz(self, f, x0, x1, p0):
        x = np.linspace(x0, x1, 100)
        y = f(x)
        Q = cumtrapz(y, x, initial=0)[-1]

        return Q * 2 * p0 / c * 1 / self.conv;
