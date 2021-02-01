class Particle(object):
    """A particle class. Gives out attributes of particles that were generated
       by the class Generator.

        Parameters
        ----------
        dataset: tuple
            Has tuple of dictionaries from the function "generate" as an input
        """

    _dataset = None

    def __init__(self, dataset):
        self.dataset = dataset

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """checks if input is list that contains dictionaries"""
        for data_entry_number in range(len(dataset)):
            if not isinstance(dataset[data_entry_number], dict):
                raise ValueError("``dataset entries`` must be dictionaries.")
        self._dataset = dataset

    def give_particle(self, particle_number):
        """gives out Origin of particle, Vector of particle and
        their Creation time of Particle from dataset"""
        particle_attributes = self._dataset[particle_number-1]
        return particle_attributes

    def give_range_of_particle(self, number_begin, number_end):
        """Gives out a range of Particles"""
        particle_list = ""
        for particle_number in range(number_begin, number_end+1):
            particle_attributes = self._dataset[particle_number]
            particle_list += particle_attributes
        return particle_list
