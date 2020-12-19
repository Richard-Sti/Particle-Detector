"""Runs the simulations and outputs data."""

import numpy
import argparse

from simulator import Detector, Generator

import setup


# Parse terminal inputs
parser = argparse.ArgumentParser(description='Runs the particle simulation.')
parser.add_argument('--Nevents', default=1000, type=int)

args = parser.parse_args()

# Initialise the generator and the detector
generator = Generator(setup.theta_max)
detectors = [Detector(setup.boundaries, setup.Npixs, setup.z0 + i * setup.dz)
             for i in range(5)]

# Get some number of events
events = generator.generate(args.Nevents)

data_names = ['xpixel', 'ypixel', 't', 'z']
ID_names = ['detectorID', 'eventID']
names = data_names + ID_names
formats = ['float64'] * 4 + ['int64'] * 2
out = numpy.zeros(args.Nevents * len(detectors),
                  dtype={'names': names, 'formats': formats})

# Processes each event at each detector and saves as numpy array
i = 0
for event in events:
    eventID = hash(frozenset(event.values()))
    for detector in detectors:
        collision = detector.evaluate_collision(event)
        detectorID = hash(frozenset(collision.values()))
        for name in data_names:
            out[name][i] = collision[name]
        out['detectorID'][i] = detectorID
        out['eventID'][i] = eventID
        i += 1

numpy.save(setup.simulation_fname, out)
print('Finished simulating the events.')
