"""Unit tests for the detector."""
import pytest

from simulator import (Generator, Detector)

PLATE = {'bounds': {'x': (-10, 10), 'y': (-10, 10)},
         'Npixs': 2000,
         'z': 30,
         'phi': 1}
NEVENTS = 100


@pytest.mark.parametrize('zs', [[10], [12, 23], [23, 25, 30]])
def test_plates_positions(zs):
    """Tests whether the detector returns the correct z-coordinate."""
    # Setup the generator
    generator = Generator(theta_max=10)
    events = generator.generate(NEVENTS)
    # Setup the detector
    plates = [PLATE.copy() for i in range(len(zs))]
    for i, z in enumerate(zs):
        plates[i]['z'] = z
    detector = Detector(plates)
    out = detector.evaluate_events(events)

    for i in range(NEVENTS):
        for j, z in enumerate(zs):
            # Check the z-coordinate
            assert out[i][j]['z'] == zs[j]
            # Check the correct thigns are stored
            for key in ('x', 'y', 'z', 't'):
                assert key in out[i][j].keys()
