# performance.py

import cProfile
import pstats

def profile_code(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        return result
    return wrapper
