from storage.queue.queue import Queue
from storage.factory_base.factory_base import FactoryBase

class QueueFactory(FactoryBase):
    def __init__(self):
        super().__init__()

    def create_instance(self):
        self.instance = Queue()