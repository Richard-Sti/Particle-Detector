"""Particle generation script."""
import numpy

from scipy.stats import truncnorm


class PoissonSource:
    r"""A Poission source. Generates events in Poisson-distributed time steps.

    Parameters
    ----------
    theta_max : float
        Maximum polar angle that defines the cone within which particles
        are generated.
    momentum_distribution : :py:class (optinal)
        A predefined simulator's momentum distribution. By default a
        truncated positive Gaussian with mean at 1 and std of 0.5.
    rate : float (optional)
        The source's emission rate.
    deg : bool (optional)
        Whether the input ``theta_max`` is in degrees.
    seed : int (optional)
        Random seed for reproducibility.
    """

    def __init__(self, theta_max, momentum_distribution=None, rate=1,
                 deg=True, seed=2021):
        self._theta_max = None
        self._rate = None
        self._deg = deg

        self.theta_max = theta_max
        self.rate = rate

        if momentum_distribution is None:
            self.momentum_distribution = TruncatedGaussian(mu=1, std=0.5)
        else:
            self.momentum_distribution = momentum_distribution
        # Set the random seed
        numpy.random.seed(seed)
        # Timestep over which emission is determined
        self._dt = 1e-5
        # Internal source time
        self._clock = 0

    @property
    def theta_max(self):
        """Returns the max polar angle in which particles are generated."""
        if self.isdeg:
            return self._theta_max * 180 / numpy.pi
        return self._theta_max

    @theta_max.setter
    def theta_max(self, theta_max):
        """Sets the maximum polar angle."""
        if not isinstance(theta_max, (float, int)):
            raise ValueError("``theta_max`` must be a float.")
        # Store the angle internally in radians
        if self.isdeg:
            theta_max *= numpy.pi / 180
        self._theta_max = theta_max

    @property
    def isdeg(self):
        """Returns whether the angular input is assumed in degrees."""
        return self._deg

    @property
    def rate(self):
        """Returns the source emission rate."""
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets ``rate``."""
        if not isinstance(rate, (float, int)):
            raise ValueError("``rate`` must be a float.")
        self._rate = rate

    def _event_times(self, T):
        """
        Returns times when the source emits a particle. Assumes Poisson
        distributed mean rate of ``self.rate``.

        Ignores the probability of emitting more than 1 particle during a
        single timestep. This is exact in the limit of small timesteps.
        """
        x = numpy.random.uniform(size=int(T/self._dt))
        # Probability of no emission within timestep self._dt
        prob0 = numpy.exp(-self.rate * self._dt)
        # Times when an event was emitted
        return self._clock + numpy.where(x > prob0)[0] * self._dt

    def _sample_sphere(self, N):
        """
        Returns uniformly distributed points on a 2-sphere within radius
        ``self.theta_max`` of the north pole.
        """
        # Cumulative distribution function
        cdf = numpy.random.uniform(0, 1, N)
        # This comes around from inverting theta's CDF
        theta = numpy.arccos(1 - cdf * (1 - numpy.cos(self._theta_max)))
        # These are uniformly distributed
        phi = numpy.random.uniform(0, 2*numpy.pi, N)
        return theta, phi

    @staticmethod
    def _spherical2cartesian(r, theta, phi):
        """Converts spherical coordinates to Cartesian."""
        stheta = numpy.sin(theta)
        x = r * stheta * numpy.cos(phi)
        y = r * stheta * numpy.sin(phi)
        z = r * numpy.cos(theta)
        return x, y, z

    def observe(self, T):
        """Observe the source for period ``T``."""
        t = self._event_times(T)
        N = t.size
        theta, phi = self._sample_sphere(N)
        momentum = self.momentum_distribution.dist.rvs(N)
        # Calling these velocities assume m=1 and no SR but fine for now
        vx, vy, vz = self._spherical2cartesian(momentum, theta, phi)

        # Bump up the internal clock
        self._clock += T
        return [{'vx': vx[i], 'vy': vy[i], 'vz': vz[i], 't': t[i],
                 'x0': 0.0, 'y0': 0.0, 'z0': 0.0} for i in range(N)]


class TruncatedGaussian:
    r"""A truncated positive Gaussian distribution.

    Parameters
    ----------
    mu : float (optional)
        Mean of the particle's truncated Gaussian momentum distribution.
    std : float (optional)
        Standard deviation of the particle's truncated Gaussian momentum
        distribution.
    """
    def __init__(self, mu, std):
        if mu <= 0:
            raise ValueError("``mu`` must be positive.")
        if std <= 0:
            raise ValueError("``std`` must be positive.")

        a = -mu/std
        b = numpy.infty
        self.dist = truncnorm(a=a, b=b, loc=mu, scale=std)
