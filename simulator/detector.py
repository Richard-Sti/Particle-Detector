"""Classes for handling the detectors and pixels in the simulation"""
import numpy


class DetectorPlate:
    r"""
    A detector plate to be installed in the detector.

    Parameters
    ----------
    bounds : dict
        Plate edges along  the x- and y-axis. Assumes detector plane spans
        the so-defined rectangle in the x and y plane.
        Example: ``{'x': (-10., 10.), 'y': (-2.0, 7.5)}``
    Npixs : int
        Total number of pixels on this detector plate.
    z : float
        Z-coordinate of the detector plate.
    phi : float (optional)
        Angle (in degrees) by which the detector plate is rotated along
        the z-axis.
    """

    def __init__(self, bounds, Npixs, z, phi=0):
        self._Npixs = None
        self._bnds = None
        self._z = None
        self._phi = None
        # Store the arguments
        self.bnds = bounds
        self.Npixs = Npixs
        self.z = z
        self.phi = phi
        # Calculate the rotation matrix
        phi = numpy.deg2rad(self.phi)
        sphi = numpy.sin(phi)
        cphi = numpy.cos(phi)
        self._rotmat = numpy.array([[cphi, -sphi],
                                    [sphi, cphi]])

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
        boundaries = boundaries.copy()
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
    def z(self):
        """Returns the detector z coordinate."""
        return self._z

    @z.setter
    def z(self, z):
        """Sets ``z``."""
        if not z > 0:
            raise ValueError("``z`` must be positive.")
        self._z = z

    @property
    def phi(self):
        """Returns the angle by which the detector plate is rotated."""
        return self._phi

    @phi.setter
    def phi(self, phi):
        """Sets ``phi``."""
        if not isinstance(phi, (float, int)):
            raise ValueError("``phi`` must be a float.")
        self._phi = phi

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
                'z': self.z}

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
        dt = (self.z - event['z0']) / event['vz']
        # Intersection point between the particle path and detector plane
        x0 = numpy.array([event['x0'] + event['vx'] * dt,
                          event['y0'] + event['vy'] * dt]).reshape(-1, 1)
        # Rotate the intersection so that detector eges || axes
        # The first rotation is with the inverse matrix because instead of
        # rotating the axes we wish to rotate the point
        x0_rot = numpy.matmul(self._rotmat.T, x0)
        # Get the pixel IDs
        pixels = self.coordinates2pixelID({p: x0_rot[i]
                                           for i, p in enumerate(['x', 'y'])})
        # Get the pixel centres Cartesian coordinates
        _xf = self.pixelID2coordinates(pixels)
        xf = numpy.array([_xf[p] for p in ('x', 'y')]).reshape(-1, 1)
        xf_rot = numpy.matmul(self._rotmat, xf)

        out = {p: xf_rot[i] for i, p in enumerate(['x', 'y'])}
        out.update({'z': self.z, 't': event['t'] + dt})
        return out


class Detector:
    r"""
    A simple particle detector consisting of several plates.

    Parameters
    ----------
    plates : list of dicts
        A list containing the individual detector planes' parameters.
        For more information see :py:class:`DetectorPlate`

    """
    def __init__(self, plates):
        self._plates = None
        self.plates = [DetectorPlate(**plate) for plate in plates]

    def evaluate_events(self, events):
        """
        Evaluates the events. Returns a list of list: ``out[i, j]``
        where the ``i`` refers to the event and ``j`` refers to the detector
        plate.
        """
        out = [None] * len(events)
        for i, event in enumerate(events):
            data = [None] * len(self.plates)
            for j, plate in enumerate(self.plates):
                data[j] = plate.evaluate_collision(event)
            out[i] = data
        return out
