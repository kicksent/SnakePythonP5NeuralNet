
'''profiling tools'''
import cProfile, pstats, io

def profile(fnc):
    
    def inner(*args, **kwargs):
        print("entered")
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        softby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(softby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner