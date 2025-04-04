import inspect
def override(method):
    """Decorator kiểm tra xem phương thức có override không"""
    method_name = method.__name__

    def wrapper(cls:object,*args,**kwargs):
        try:
            parents = inspect.getmro(cls.__class__)[1:-1]
            if not any((hasattr(pr,method_name) for pr in parents )):raise TypeError(f"Method '{method_name}' does not override any method in base class.")
            return method(cls,*args,**kwargs)
        except Exception as e:
            raise TypeError(f"Method '{method_name}' does not override any method in base class.")

    return wrapper

class parent:
    def __init__(self):
        self.a  = 1
    
    def selfprint(self):
        print(self.a)
    

class child(parent):
    def __init__(self):
        super().__init__()
        self.b = 2
    @override
    def selfprintf(self):
        print(self.b)

ch = child()
ch.selfprint()
