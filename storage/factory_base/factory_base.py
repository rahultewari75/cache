class FactoryBase:
    def __init__(self):
        self.instance = None

    def create_instance(self, *args, **kwargs):
        pass

    def get_instance(self):
        return self.instance
    
    def reset_instance(self):
        self.instance = None
    
    def instance_exists(self) -> bool:
        return self.instance is not None