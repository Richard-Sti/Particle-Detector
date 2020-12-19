"""Unit tests the generator."""
import numpy

import pytest

from simulator import Generator

THETA_MAX = 10
NEVENTS = 1000

@pytest.mark.parametrize('theta_max', [5, 10, 25])
def test_max_angle(theta_max):
    """Tests the max polar angle in which events are generated."""
    generator = Generator(theta_max)
    events = generator.generate(NEVENTS)

    for event in events:
        v = numpy.linalg.norm([event[p] for p in ('vx', 'vy', 'vz')])
        theta = numpy.arccos(event['vz'] / v) * 180 / numpy.pi
        assert theta < theta_max


@pytest.mark.parametrize('t0', [0])
def test_event_times(t0):
    """Tests that event times are sequential."""
    generator = Generator(THETA_MAX)
    events = generator.generate(NEVENTS)

    t = t0 - 1e-12
    for event in events:
        assert event['t'] > t
        t = event['t']


@pytest.mark.parametrize('nevents', [25])
def test_event_outputs(nevents):
    """Tests whether all expected event data is generated."""
    generator = Generator(THETA_MAX)
    events = generator.generate(nevents)
    test_params = ['vx', 'vy', 'vz', 't', 'x0', 'y0', 'z0']
    for event in events:
        assert all(p in test_params for p in event.keys())
        assert all(event[p] is not None for p in event.keys())
