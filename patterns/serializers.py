from jsonpickle import dumps, loads


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj
        
    def save(self):
        return dumps(self.obj)
    
    @staticmethod
    def load(obj):
        return loads(obj)