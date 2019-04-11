'''
# Start timer
my_timer = Timer()

# Get time string:
time_hhmmss = my_timer.get_time_hhmmss()
print("Time elapsed: %s" % time_hhmmss )

# ... use the timer again
my_timer.restart()

# Get time:
time_hhmmss = my_timer.get_time_hhmmss()

'''
import time

class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_time_hhmmss(self):
        end = time.time()
        m, s = divmod(end - self.start, 60)
        h, m = divmod(m, 60)
        time_str = "%02d:%02d:%02d" % (h, m, s)
        return time_str
