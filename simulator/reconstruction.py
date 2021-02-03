"""Vector reconstructtion script."""
import numpy
from itertools import combinations
from scipy.special import comb


class Reconstructor(object):
    r"""
    Particle velocity and speed reconstructor. Calculates the velocity
    between all possible pairs of detector plates and returns the average
    velocity.
    """

    def __init__(self):
        pass

    @staticmethod
    def ang_dist(event):
        phi = numpy.arctan2(event['vy'], event['vx'])
        theta = numpy.arccos(event['vz'] / event['v'])
        return {'phi': phi, 'theta': theta}

    @staticmethod
    def pair_velocity(pair):
        """Calculates the velocity between a pair of detector pixels."""
        ds = numpy.array([pair[1][p] - pair[0][p] for p in ('x', 'y', 'z')])
        dt = abs(pair[1]['t'] - pair[0]['t'])
        velocity = ds / dt
        return velocity

    def reconstruct(self, data):
        """
        Reconstructs the averaged velocity and speed of events.
        """
        out = [None] * len(data)
        # Get the speed and velocities
        for i, event in enumerate(data):
            stats = {}
            v = numpy.empty(shape=(comb(len(event), 2, exact=True), 3))
            for j, pair in enumerate(combinations(event, 2)):
                v[j, :] = self.pair_velocity(pair)
            # Append the speed
            stats.update({'v': numpy.linalg.norm(v, axis=1).mean()})
            # Calculate the mean velocity
            v = numpy.mean(v, axis=0)
            stats.update({p: v[k] for k, p in enumerate(['vx', 'vy', 'vz'])})
            out[i] = stats
        # Get the angular distribution
        for event in out:
            event.update(self.ang_dist(event))
        return out
