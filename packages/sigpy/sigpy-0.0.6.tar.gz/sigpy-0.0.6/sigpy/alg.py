# -*- coding: utf-8 -*-
"""This module provides an abstract class Alg for iterative algorithms,
and implements commonly used methods.
"""
import numpy as np
from sigpy import backend, util, config

if config.cupy_enabled:
    import cupy as cp


class Alg(object):
    """Abstraction for iterative algorithms.

    The standard way of using an Alg object, say alg, is as follows:

    >>> while not alg.done():
    >>>     alg.update()

    The user is free to run other things in the while loop.
    An Alg object is meant to run once. Once done, the object should not be run again.

    When creating a new Alg class, the user should supply an _update() function
    to perform the iterative update, and optionally a _done() function
    to determine when to terminate the iteration. The default _done() function
    simply checks whether the number of iterations has reached the maximum.

    The interface for each Alg class should not depend on Linop or Prox explicitly.
    For example, if the user wants to design an Alg class to accept a Linop, say A,
    as an argument, then it should also accept any function that can be called
    to compute x -> A(x). Similarly, to accept a Prox, say proxg, as an argument,
    the Alg class should accept any function that can be called to compute
    alpha, x -> proxg(x).

    Args:
        max_iter (int): Maximum number of iterations.
        device (int or Device): Device.

    """
    def __init__(self, max_iter, device):
        self.max_iter = max_iter
        self.device = backend.Device(device)    
        self.iter = 0

    def _update(self):
        raise NotImplementedError

    def _done(self):
        return self.iter >= self.max_iter

    def update(self):
        if self.done():
            raise RuntimeError('Alg is already done. One reason for this error '
                               'is that you are running the Alg object twice.'
                               'Each Alg object is only meant to be run once.'
                               'Please consider creating a new Alg.')
            
        with self.device:
            self._update()
            self.iter += 1

    def done(self):
        with self.device:
            return self._done()


class PowerMethod(Alg):
    """Power method to estimate maximum eigenvalue and eigenvector.

    Args:
        A (Linop or function): Function to a hermitian linear mapping.
        x (array): Variable to optimize over.
        max_iter (int): Maximum number of iterations.

    Attributes:
        max_eig (float): Maximum eigenvalue of `A`.

    """
    def __init__(self, A, x, max_iter=30):
        self.A = A
        self.x = x
        self.max_eig = np.infty
        super().__init__(max_iter, backend.get_device(x))

    def _update(self):
        y = self.A(self.x)
        self.max_eig = util.asscalar(util.norm(y))
        if self.max_eig == 0:
            self.x.fill(0)
        else:
            backend.copyto(self.x, y / self.max_eig)

    def _done(self):
        return self.iter >= self.max_iter or self.max_eig == 0


class ProximalPointMethod(Alg):
    """Proximal point method.

    """
    def __init__(self, proxf, alpha, x, max_iter=100, device=backend.cpu_device):
        self.proxf = proxf
        self.alpha = alpha
        self.x = x
        
        super().__init__(max_iter, device=device)

    def _update(self):
        backend.copyto(self.x, self.proxf(self.alpha, self.x))


class GradientMethod(Alg):
    """First order gradient method.

    Considers the composite cost function:

    .. math:: f(x) + g(x)

    where f is smooth, and g is simple, ie proximal operator of g is simple to compute.

    Args:
        gradf (function): function to compute gradient of f.
        x (array): variable to optimize over.
        alpha (float): step size.
        proxg (Prox, function or None): Prox or function to compute proximal mapping of g.
        accelerate (bool): toggle Nesterov acceleration.
        P (Linop, function or None): Linop or function to precondition input, 
            assumes proxg has already incorporated P.
        max_iter (int): maximum number of iterations.

    References:
        Nesterov, Y. E. (1983). 
        A method for solving the convex programming problem with convergence rate 
        O (1/k^ 2). In Dokl. Akad. Nauk SSSR (Vol. 269, pp. 543-547).

        Beck, A., & Teboulle, M. (2009). 
        A fast iterative shrinkage-thresholding algorithm for linear inverse problems. 
        SIAM journal on imaging sciences, 2(1), 183-202.

    """
    def __init__(self, gradf, x, alpha, proxg=None,
                 accelerate=False, max_iter=100):
        self.gradf = gradf
        self.alpha = alpha
        self.accelerate = accelerate
        self.proxg = proxg
        self.x = x
        
        if self.accelerate:
            self.z = self.x.copy()
            self.t = 1

        if self.accelerate or self.proxg is not None:
            self.x_old = self.x.copy()

        self.resid = np.infty
        super().__init__(max_iter, backend.get_device(x))

    def _update(self):
        if self.accelerate or self.proxg is not None:
            backend.copyto(self.x_old, self.x)

        if self.accelerate:
            backend.copyto(self.x, self.z)

        gradf_x = self.gradf(self.x)
            
        util.axpy(self.x, -self.alpha, gradf_x)

        if self.proxg is not None:
            backend.copyto(self.x, self.proxg(self.alpha, self.x))

        if self.accelerate:
            t_old = self.t
            self.t = (1 + (1 + 4 * t_old**2)**0.5) / 2
            backend.copyto(self.z, self.x + (t_old - 1) / self.t * (self.x - self.x_old))

        if self.accelerate or self.proxg is not None:
            self.resid = util.asscalar(util.norm((self.x - self.x_old) / self.alpha**0.5))
        else:
            self.resid = util.asscalar(util.norm(gradf_x))

    def _done(self):
        return (self.iter >= self.max_iter) or self.resid == 0


class ConjugateGradient(Alg):
    r"""Conjugate Gradient Method. Solves for:

    .. math:: A x = b

    where A is hermitian.

    Args:
        A (Linop or function): Linop or function to compute A.
        b (array): Observation.
        x (array): Variable.
        P (function or None): Preconditioner.
        max_iter (int): Maximum number of iterations.

    """
    def __init__(self, A, b, x, P=None, max_iter=100):
        self.A = A
        self.P = P
        self.x = x
        device = backend.get_device(x)
        with device:
            self.r = b - self.A(self.x)

            if self.P is None:
                z = self.r
            else:
                z = self.P(self.r)

            if max_iter > 1:
                self.p = z.copy()
            else:
                self.p = z

        self.zero_gradient = False
        self.rzold = util.dot(self.r, z)
        self.resid = util.asscalar(self.rzold**0.5)
        super().__init__(max_iter, device)

    def _update(self):
        Ap = self.A(self.p)
        pAp = util.dot(self.p, Ap)
        if pAp == 0:
            self.zero_gradient = True
            return

        self.alpha = self.rzold / pAp
        util.axpy(self.x, self.alpha, self.p)
        if self.iter < self.max_iter - 1:
            util.axpy(self.r, -self.alpha, Ap)
            if self.P is not None:
                z = self.P(self.r)
            else:
                z = self.r
                
            rznew = util.dot(self.r, z)
            beta = rznew / self.rzold
            util.xpay(self.p, beta, z)
            self.rzold = rznew

        self.resid = util.asscalar(self.rzold**0.5)

    def _done(self):
        return (self.iter >= self.max_iter) or self.zero_gradient or self.resid == 0


class PrimalDualHybridGradient(Alg):
    r"""Primal dual hybrid gradient.

    Considers the problem:

    .. math:: \min_x \max_u - f^*(u) + g(x) + h(x) + <Ax, u>

    Or equivalently:

    .. math:: \min_x f(A x) + g(x) + h(x)

    where f, and g are simple, and h is Lipschitz continuous.

    Args:
        proxfc (function): Function to compute proximal operator of f^*.
        proxg (function): Function to compute proximal operator of g.
        A (function): Function to compute a linear mapping.
        AH (function): Function to compute the adjoint linear mapping of `A`.
        x (array): Primal solution.
        u (array): Dual solution.
        tau (float or array): Primal step-size.
        sigma (float or array): Dual step-size.
        gamma_primal (float): Strong convexity parameter of g.
        gamma_dual (float): Strong convexity parameter of f^*.
        max_iter (int): Maximum number of iterations.

    References:
       Chambolle, A., & Pock, T. (2011).
       A first-order primal-dual algorithm for convex problems with 
       applications to imaging. Journal of mathematical imaging and vision, 40(1), 120-145.

    """
    def __init__(self, proxfc, proxg, A, AH, x, u,
                 tau, sigma, theta=1, gradh=None,
                 gamma_primal=0, gamma_dual=0,
                 max_iter=100):
        self.proxfc = proxfc
        self.proxg = proxg
        self.gradh = gradh

        self.A = A
        self.AH = AH

        self.u = u
        self.x = x

        self.tau = tau
        self.sigma = sigma
        self.theta = theta
        self.gamma_primal = gamma_primal
        self.gamma_dual = gamma_dual
        
        self.x_ext = self.x.copy()
        self.u_old = self.u.copy()
        self.x_old = self.x.copy()
        self.resid = np.infty

        super().__init__(max_iter, backend.get_device(x))

    def _update(self):
        backend.copyto(self.u_old, self.u)
        backend.copyto(self.x_old, self.x)

        # Update dual.
        delta_u = self.A(self.x_ext)
        util.axpy(self.u, self.sigma, delta_u)
        backend.copyto(self.u, self.proxfc(self.sigma, self.u))

        # Update primal.
        delta_x = self.AH(self.u)
        if self.gradh is not None:
            delta_x += self.gradh(self.x)
            
        util.axpy(self.x, -self.tau, delta_x)
        backend.copyto(self.x, self.proxg(self.tau, self.x))

        # Update step-size if neccessary.
        xp = self.device.xp
        if self.gamma_primal > 0 and self.gamma_dual == 0:
            theta = 1 / (1 + 2 * self.gamma_primal * xp.amin(xp.abs(self.tau)))**0.5
            self.tau *= theta
            self.sigma /= theta
        elif self.gamma_primal == 0 and self.gamma_dual > 0:
            theta = 1 / (1 + 2 * self.gamma_dual * xp.amin(xp.abs(self.sigma)))**0.5
            self.tau /= theta
            self.sigma *= theta
        else:
            theta = self.theta

        # Extrapolate primal.
        x_diff = self.x - self.x_old
        backend.copyto(self.x_ext, self.x + theta * x_diff)

        u_diff = self.u - self.u_old
        self.resid = util.asscalar(util.norm2(x_diff / self.tau**0.5) +
                                   util.norm2(u_diff / self.sigma**0.5))**0.5


class AltMin(Alg):
    """Alternating Minimization.

    Args:
        min1 (function): Function to minimize over variable 1.
        min2 (function): Funciton to minimize over variable 2.
        max_iter (int): Maximum number of iterations.

    """
    def __init__(self, min1, min2, max_iter=30):
        self.min1 = min1
        self.min2 = min2
        super().__init__(max_iter, backend.cpu_device)

    def _update(self):
        self.min1()
        self.min2()
