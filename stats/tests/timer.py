import time
class TimeIt:
    
    @staticmethod
    def executionTime(f):
        def wrapper(*args, **kwargs):
            startTime = time.time()
            f(*args,**kwargs)
            print("%s finished executing in %s seconds" % (f.__name__, time.time()-startTime))
        return wrapper