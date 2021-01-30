"""Example code to show how the detector works."""
import numpy

from simulator import (Detector, PoissonSource, TruncatedGaussian)



# Initialise the source
source = PoissonSource(theta_max=10, rate=1, seed=33)

# Initialise some detector plates
plate1 = {'bounds': {'x': (-20, 20), 'y': (-20, 20)},
         'Npixs': 2000,
         'z': 30,
         'phi': 20}

plate2 = {'bounds': {'x': (-20, 20), 'y': (-20, 20)},
         'Npixs': 2000,
         'z': 35,
         'phi': 0}

plate3 = {'bounds': {'x': (-20, 20), 'y': (-20, 20)},
         'Npixs': 2000,
         'z': 40,
         'phi': 0}

plate4 = {'bounds': {'x': (-20, 20), 'y': (-20, 20)},
         'Npixs': 2000,
         'z': 45,
         'phi': 0}

plate5 = {'bounds': {'x': (-20, 20), 'y': (-20, 20)},
         'Npixs': 2000,
         'z': 50,
         'phi': 0}

plates = [plate1, plate2, plate3, plate4, plate5]

# Initialise the detector
detector = Detector(plates)

events = source.observe(T=3)  # Observe the source for 10 time units


out = detector.evaluate_events(events)

print(out)

# Loop over the events
for i, event in enumerate(out):
    # Loop over what detector plates returned
    for j, interaction in enumerate(event):
        print("Event {}, plate {}:".format(i, j))
        print(interaction)




'''
Vector reconstruction script.

Current functoionality, under assumption, that there is only one particle in
detector space (z =[30, 50]) at all time:
    sorts Event by time. Then creates a new list for pairs of events of the highest
    and lowest detection coordinate z for every particle. Converts the list of
    dictionarys into a list of numpy arrays. Substracts related event vectors to
    recreate a flight vector.
    Conversion into a dictionary of the format of the actual particles flight vectors.

    
########## for Liang: ########################

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
        vector_reprod = {'vx': 0, 'vy': 0, 'vz': 0, 't': 0, '|v|': 0}
        vector_reprod['vx'] = vector_recon[0]/100/vector_recon[2]
        vector_reprod['vy'] = vector_recon[1]/100/vector_recon[2]
        vector_reprod['vz'] = vector_recon[3]/vector_recon[2]        
        vector_reprod['t'] = vector1[2] - vector1[3]/vector_recon[3]*vector_recon[2]
        vector_reprod['|v|'] = 
        return vector_reprod
   
    def data_sorting(self, data_list):
        timesorted_data = sorted(data_list, key = lambda i: i['t'])
        sorted_data =[]
        for i in range(len(timesorted_data)):
            if timesorted_data[i]['z'] == 30:
                sorted_data.append(timesorted_data[i])
            elif timesorted_data[i]['z'] == 35 and timesorted_data[i-1]['z'] != 30:
                sorted_data.append(timesorted_data[i])
            elif timesorted_data[i]['z'] == 40 and ((timesorted_data[i-2]['z'] != 30 and timesorted_data[i-1]['z'] != 35) or (timesorted_data[i+1]['z'] != 45 and timesorted_data[i+2]['z'] != 50)):
                sorted_data.append(timesorted_data[i])
            elif timesorted_data[i]['z'] == 45 and timesorted_data[i+1]['z'] != 50:
                sorted_data.append(timesorted_data[i])
            elif timesorted_data[i]['z'] == 50:
                sorted_data.append(timesorted_data[i])
        return sorted_data



    def reconstruct(self, data_list):
        event_vectors = []
        sorted_data_list = self.data_sorting(data_list)
        if len(sorted_data_list) % 2 != 0:
            raise ValueError('irreconstructable set of data. Too much noise, too little events')
        for data in sorted_data_list:
            recon_vec = self.event2vector(data)
            event_vectors.append(recon_vec)
        reconstructed_data = []
        for i in range(0, len(event_vectors), 2):
            reconstructed_data.append(self.vector_reconstruct(event_vectors[i], event_vectors[i+1]))
        return reconstructed_data
    

