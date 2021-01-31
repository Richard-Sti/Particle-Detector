"""Unit tests for the detector."""
import pytest

from simulator import (PoissonSource, Detector)

PLATE = {'bounds': {'x': (-10, 10), 'y': (-10, 10)},
         'Npixs': 2000,
         'z': 30,
         'phi': 23}
T = 10
THETA_MAX = 10
RATE = 10


@pytest.mark.parametrize('zs', [[10], [12, 23], [23, 25, 30]])
def test_plates_positions(zs):
    """Tests whether the detector returns the correct z-coordinate."""
    # Setup the generator
    source = PoissonSource(THETA_MAX, rate=RATE)
    events = source.observe(T)
    # Setup the detector
    plates = [PLATE.copy() for i in range(len(zs))]
    for i, z in enumerate(zs):
        plates[i]['z'] = z
    detector = Detector(plates)
    out = detector.evaluate_events(events)
    N = len(events)

    for i in range(N):
        for j, z in enumerate(zs):
            # Check the z-coordinate
            assert out[i][j]['z'] == zs[j]
            # Check the correct thigns are stored
            for key in ('x', 'y', 'z', 't'):
                assert key in out[i][j].keys()
