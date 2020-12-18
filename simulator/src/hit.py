"""judging whether a hit happens"""
import numpy,  pickle
import sys


particles = pickle.load(open("{}".format(sys.argv[1]), "rb"))


class Hit(object):
    def __init__(self, conf):
        success, module = utils.io.load_condor()
        if not success:
            print("Could not run simulation")
            return

        self._is_hit = None


    def hit(self):
        self._output = self.e.propagate()
        self._is_hit = True

    def miss(self):
        self._is_hit = False

    def get_is_hit(self):
        return self._is_hit

    def next_event(self):
        if numpy.random.rand() < self.hitrate: self.hit()
        else: self.miss()

for particleIt in particles:
    particle = particles[particleIt]
    particle.PrintBasic()

    for detector in particle.Detectors:
        print "  Hit detector {} with momentum {}".format(detector, particle.Detectors[detector].Pz)
