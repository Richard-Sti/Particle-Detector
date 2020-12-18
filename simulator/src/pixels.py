"""Classes for handling the detectors and pixels in the simulation"""
import numpy


class Detector(object):
    r"""
    Lalalalalala.
    """
    _Npixs = None
    _bnds = None
    _zdist = None

    def __init__(self, boundaries, Npixs, zdist):
        self.bnds = boundaries
        self.Npixs = Npixs
        self.zdist = zdist

    @property
    def Npixs(self):
        """Returns the number of pixels in this detector."""
        return self._Npixs

    @Npixs.setter
    def Npixs(self, Npixs):
        """Sets the number of pixels."""
        if not isinstance(Npixs, int):
            raise ValueError("``Npixs`` must be an integer.")
        self._Npixs = Npixs

    @property
    def bnds(self):
        """Returns the detector boundaries in the ``x`` and ``y`` plane."""
        return self._bnds

    @bnds.setter
    def bnds(self, boundaries):
        """Sets ``bnds``. Checks that both ``x`` and ``y`` bounds
        are present."""
        if not isinstance(boundaries, dict):
            raise ValueError("``boundaries`` must be a dictionary.")
        xbnd = boundaries.pop('x', None)
        ybnd = boundaries.pop('y', None)
        if boundaries:
            raise ValueError("Unknown keys: {}".format(boundaries.keys()))
        self._bnds = {}
        for par, bnd in zip(['x', 'y'], [xbnd, ybnd]):
            if bnd is None:
                raise ValueError("Boundaries must include {}".format(par))
            if len(bnd) != 2:
                raise ValueError("Specific boundaries must have length 2.")
            self._bnds[par] = sorted(bnd)

    @property
    def zdist(self):
        """Returns the detector z coordinate."""
        return self._zdist

    @zdist.setter
    def zdist(self, zdist):
        """Sets ``zdist``."""
        if not zdist > 0:
            raise ValueError("``zdist`` must be positive.")
        self._zdist = zdist

    def pixelID2coordinates(self, IDs):
        """
        Returns the Cartesian coordinates ``i``-th horizontal and ``j``-th
        vertical pixel.
        """
        i, j = IDs['xpixel'], IDs['ypixel']
        if not (0 <= i < self.Npixs and 0 <= j < self.Npixs):
            raise ValueError("Invalid pixel ID.")
        # Remember that i, j run from 0, 1, ..., Npixs - 1.
        xbnd = self.bnds['x']
        ybnd = self.bnds['y']
        return {'x': (xbnd[1] - xbnd[0]) / self.Npixs * (i + 0.5) + xbnd[0],
                'y': (ybnd[1] - ybnd[0]) / self.Npixs * (j + 0.5) + ybnd[0],
                'z': self.zdist}

    def coordinates2pixelID(self, coords):
        """
        Returns the ID of a pixel that corresponds to the given x and y
        coordinates. Checks that both are within the detector area.
        """
        IDs = {}
        for par, bnd in self.bnds.items():
            if not bnd[0] < coords[par] < bnd[1]:
                raise ValueError("Invalid position.")
            # Later move these somewhere so they don't get regenerated
            # every time
            width = bnd[1] - bnd[0]
            bins = numpy.arange(bnd[0], bnd[1], width / self.Npixs)
            IDs['{}pixel'.format(par)] = numpy.digitize(coords[par], bins) - 1
        return IDs

    def evaluate_collision(self, event):
        """
        Evaluates the collision with a simulated event. Returns the ID of
        a pixel that is hit and the time.
        """
        dt = (self.zdist - event['z0']) / event['vz']
        # Cartesian coordinates
        coords = {'x': event['x0'] + event['vx'] * dt,
                  'y': event['y0'] + event['vy'] * dt,}
        # Get the pixel IDs
        data = self.coordinates2pixelID(coords)
        data.update({'t': event['t']+ dt})
        return data
