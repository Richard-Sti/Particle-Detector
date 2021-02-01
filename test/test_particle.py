"""Unit tests for the particle."""
import pytest
from simulator import (PoissonSource, Particle)

T = 10
THETA_MAX = 10
RATE = 10


@pytest.mark.parametrize('particle_number', [1, 10, 20])
def test_particle_attributes(particle_number):
    """Tests whether particle returns correct value of a unit in Generator."""
    # Setup the generator
    source = PoissonSource(THETA_MAX, rate=RATE)
    events = source.observe(T)
    # Setup the Particle
    from simulator import Particle
    particle = Particle(events)
    out = particle.give_particle(particle_number)
    assert out == events[particle_number-1]


@pytest.mark.parametrize('number_begin', [0, 5, 10])
@pytest.mark.parametrize('number_end', [15, 20, 25])
def test_particle_attributes(number_begin, number_end):
    """Tests whether particles return correct values of Generator."""
    # Setup the generator
    source = PoissonSource(THETA_MAX, rate=RATE)
    events = source.observe(T)
    # Setup the Particle
    from simulator import Particle
    particle = Particle(events)
    out = particle.give_range_of_particle(number_begin, number_end)
    N = len(events)

    if N > number_end:
        for i in range(len(out)):
            # Check if the correct things are stored
            for key in ('vx', 'vy', 'vz', 't', 'x0', 'y0', 'z0'):
                assert key in out[i].keys()
