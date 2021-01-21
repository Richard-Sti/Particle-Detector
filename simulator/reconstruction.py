'''
from setup import *
from simulator import (Generator, Detector)
'''

import numpy

'''
Vector reconstruction script.

Current functoionality, under assumption, that there is only one particle in
detector space (z =[30, 50]) at all time:
    sorts Event by time and subtracts related events with highest possible physical
    distance.
    So usually the event from the first and fifth detector. If one of those events
    is not sxisting (detector noise), then it takes the next best instead.
    
########## for Liang: #########################

Idea of a reconstruction mechanism for multiple patricles in detector space
at the same Time:

Tries to reconstruct the particle vector by connecting the events of the
different detectors at z = 30, 35, 40, 45, 50.

    For each event in the first detector the following things happen:
        A vector to a event in the second detector is created. This also
        includes time. This vector is used to find a path matching pixel in
        the next detector plane. That pixel and all adjacent are then checked
        for events with suiting timestamps.
        
            If there are no matching event, the vector gets deleted from the
            reconstruction data file.
            
            If there are events for one or multible pixels stored with
            matching time, the process is repeated to the next detectors
            pixels and so on.
            
            If all of the three following detectors show matching events, the
            reconstruction of the vector must be a success. A vector from the
            pixel in the first detector the the pixel in the last detector is
            stored in a list. All the events that are part of a succesfull
            reconstruction are then deleted from the Event data file (a copy).
        
        This works under the following assumptions that:
            1. there is no change of velocity or direction after each hit.


'''

class Reconstructor(object):
    
    def __init__(self, event_data=None):
        self.event_data = None
        

# Methods:
    
    def event2vector(self, event):
        event_vector = numpy.array([])
        for value in event.values():
            event_vector = numpy.append(event_vector, value)
        return event_vector
    
    def vector2event(self, vector):
        
        event = {'xpixel': vector[0], 'ypixel': vector[1], 'zpixel': vector[2], 't':  vector[3]}
        return event 
           
    """  already existing and working function that gives out a list of possibly hit
    pixels in the following detector plane:
        
        
    def pixel_reach(self, event1, event2):
        ''' gives out a list of possible events in the next detector plane'''
        list_events = []
        neighbours = [-1, 0, 1]
        event1_vector = self.event2vector(event1)
        event2_vector = self.event2vector(event2)
        zgap = event2_vector[2] - event1_vector[2]
        next_event_vector = 5 * (2 * event2_vector - event1_vector )/ zgap
        for xpixel, in neighbours:
            for ypixel in neighbours:
                list_events.append(self.vector2event(next_event_vector + numpy.array([xpixel, 0, 0, 0]) + numpy.array([0, ypixel, 0, 0])))
        return list_events
    """
    
    def vector_reconstruct(self, vector1, vector2):
        vector_recon = vector2 - vector1
        vector_reprod = {'vx': 0, 'vy': 0, 'vz': 0, 't': 0}
        vector_reprod['vx'] = vector_recon[0]/100/vector_recon[2]
        vector_reprod['vy'] = vector_recon[1]/100/vector_recon[2]
        vector_reprod['vz'] = vector_recon[3]/vector_recon[2]        
        vector_reprod['t'] = vector1[2] - vector1[3]/vector_recon[3]*vector_recon[2]
        return vector_reprod

    def reconstruct(self, data_list):
        sorted_data = sorted(data_list, key = lambda i: i['t'])
        event_vectors = []
        for data in sorted_data:
            recon_vec = self.event2vector(data)
            event_vectors.append(recon_vec)
        reconstructed_data = []
        for i in range(0, len(event_vectors), 5):
            reconstructed_data.append(self.vector_reconstruct(event_vectors[i], event_vectors[i+4]))
        return reconstructed_data
    
    

""" simulation:

generator = Generator(theta_max)    # theta_max = 10
recon = Reconstructor()

event_data = []

 # generation of N=1 particles:
events = generator.generate(N=3)


print("Actual Particle: ", events)

for i in range(z0, 51, dz):
    detector = Detector(boundaries, Npixs, i)
    detections = [detector.evaluate_collision(event) for event in events]
    event_data = event_data + detections
   

print(recon.reconstruct(event_data))

"""

