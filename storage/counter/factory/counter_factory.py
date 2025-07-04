from storage.factory_base.factory_base import FactoryBase
from storage.counter.counter import Counter

class CounterFactory(FactoryBase):
    def __init__(self):
        super().__init__()

    def create_instance(self):
        self.instance = Counter()
    