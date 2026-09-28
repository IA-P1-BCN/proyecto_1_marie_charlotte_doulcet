from abc import ABC, abstractmethod 

class Storage(ABC):

    @abstractmethod
    def save_ride(self, ride):
      pass

    @abstractmethod
    def load_today(self):
      pass

  