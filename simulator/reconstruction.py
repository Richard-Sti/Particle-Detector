import numpy

'''
Vector reconstruction script.

Current functoionality, under assumption, that there is only one particle in
detector space (z =[30, 50]) at all time:
    sorts Event by time. Then creates a new list for pairs of events of the highest
    and lowest detection coordinate z for every particle. Converts the list of
    dictionarys into a list of numpy arrays. Substracts related event vectors to
    recreate a flight vector.
    Conversion into a dictionary of the format of the actual particles flight vectors.
    
Use: create object reconstructor = Reconstructor()
of the class to use the reconstructor.reconstruct(detector_output) method.

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
        
        event = {'xpixel': vector[0], 'ypixel': vector[1], 'zpixel': vector[2], 't': vector[3]}
        return event 
    
    def vector_reconstruct(self, vector1, vector2):
        vector_recon = vector2 - vector1
        vector_reprod = {'vx': 0, 'vy': 0, 'vz': 0, 't': 0, '|v|': 0}
        vector_reprod['vx'] = vector_recon[0]/vector_recon[3]
        vector_reprod['vy'] = vector_recon[1]/vector_recon[3]
        vector_reprod['vz'] = vector_recon[2]/vector_recon[3]        
        vector_reprod['t'] = vector1[3] - vector1[2]/vector_recon[2]*vector_recon[3]
        vector_reprod['|v|'] = numpy.sqrt(vector_reprod['vx']**2 + vector_reprod['vy']**2 +vector_reprod['vz']**2)
        return vector_reprod
    
    
    def reconstruct(self, data_list):
        reconstructed_data = []
        for list in data_list:
            detections = len(list)
            first_det = self.event2vector(list[0])
            final_det = self.event2vector(list[detections - 1])
            reconstructed_data.append(self.vector_reconstruct(first_det, final_det))                                      
        return reconstructed_data