import time

class WorkoutTimer:
    def __init__(self, stop_delay=2):
        self.stop_delay = stop_delay
        self.total_time = 0
        self.start_time = None
        self.last_active_time = None
        self.active = False

    def start(self):
        if not self.active:
            self.active = True
            self.start_time = time.time()

    def mark_activity(self):
        self.start()
        self.last_active_time = time.time()

    def update(self):
        if self.active and self.last_active_time:
            if time.time() - self.last_active_time > self.stop_delay:
                self.total_time += time.time() - self.start_time
                self.active = False
                self.start_time = None

    def get_time(self):
        if self.active:
            return self.total_time + (time.time() - self.start_time)
        return self.total_time