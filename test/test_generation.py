"""Unit tests the generator."""
import numpy

import pytest
from simulator import (PoissonSource, TruncatedGaussian)

THETA_MAX = 10
T = 10
RATE = 10


@pytest.mark.parametrize('theta_max', [5, 10, 25])
def test_max_angle(theta_max):
    """Tests the max polar angle in which events are generated."""
    source = PoissonSource(theta_max, rate=RATE)
    events = source.observe(T)

    for event in events:
        v = numpy.linalg.norm([event[p] for p in ('vx', 'vy', 'vz')])
        theta = numpy.arccos(event['vz'] / v) * 180 / numpy.pi
        assert theta < theta_max


@pytest.mark.parametrize('t0', [0])
def test_event_times(t0):
    """Tests that event times are sequential."""
    source = PoissonSource(THETA_MAX, rate=RATE)
    events = source.observe(T)

    t = t0 - 1e-12
    for event in events:
        assert event['t'] > t
        t = event['t']


@pytest.mark.parametrize('t', [5, 10, 33])
def test_event_outputs(t):
    """Compare expected output labels."""
    source = PoissonSource(THETA_MAX, rate=RATE)
    events = source.observe(t)
    test_params = ['vx', 'vy', 'vz', 't', 'x0', 'y0', 'z0']
    for event in events:
        assert all(p in test_params for p in event.keys())
        assert all(event[p] is not None for p in event.keys())


@pytest.mark.parametrize('mu', [0.5, 1, 30])
@pytest.mark.parametrize('std', [0.3, 1])
def test_momentum_mean(mu, std):
    """Tests the mean of the momentum distribution."""
    dist = TruncatedGaussian(mu, std)
    source = PoissonSource(THETA_MAX, momentum_distribution=dist, rate=100)
    events = source.observe(100)
    x = [None] * len(events)
    for i, event in enumerate(events):
        x[i] = sum([event[p]**2 for p in ['vx', 'vy', 'vz']])**0.5
    # Let's go for a absolute relatively low tolerance..
    assert numpy.isclose(numpy.mean(x), dist.dist.stats('m'), atol=1e-1)
