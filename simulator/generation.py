"""Particle generation script."""
import numpy


class Generator(object):

    r"""A particle generator. Randomly generates a particle within some
    cone with a given momentum distribution.

    Parameters
    ----------
    theta_max : float
        Maximum polar angle that defines the cone within which particles
        are generated.
    momentum_distribution : :py:class:`scipy.stats`
        A probability distribution from which particle momenta are drawn.
        Must be from `scipy.stats.`
    deg : bool
        Whether the input ``theta_max`` is in degrees.
    seed : int
        Random seed for reproducibility.
    """

    _theta_max = None
    _deg = None

    def __init__(self, theta_max, momentum_distribution=None, deg=True,
                 seed=2021):
        self._deg = deg
        self.theta_max = theta_max
        # Store the momentum dsitribution.. generalise this later
        self.momentum_distribution = None
        # Set the random seed
        numpy.random.seed(seed)

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

    def generate(self, N=1):
        """Generates ``N`` random flight vectors with a given momentum."""
        cdf = numpy.random.uniform(0, 1, N)

        theta = numpy.arccos(1 - cdf * (1 - numpy.cos(self._theta_max)))
        phi = numpy.random.uniform(0, 2*numpy.pi, N)
        # Add a randomly drawn time separation between events
        dt = numpy.cumsum(numpy.random.uniform(size=N))
        # Translate such that dt[0] is at 0
        dt -= dt[0]
        # Start drawing from some scipy.stats class
        p = 1
        # Convert to Cartesians
        stheta = numpy.sin(theta)
        vx = p * stheta * numpy.cos(phi)
        vy = p * stheta * numpy.sin(phi)
        vz = p * numpy.cos(theta)
        # Later make it possible to change the initial coordinates
        return [{'vx': vx[i], 'vy': vy[i], 'vz': vz[i], 't': dt[i], 'x0': 0.0,
                 'y0': 0.0, 'z0': 0.0} for i in range(N)]
