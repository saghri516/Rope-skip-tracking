import time

class SessionManager:
    def __init__(self, stop_delay):
        self.stop_delay = stop_delay
        self.total_time = 0
        self.session_start = None
        self.active = False
        self.last_jump_time = None

    def start(self):
        if not self.active:
            self.active = True
            self.session_start = time.time()

    def update_jump(self):
        self.last_jump_time = time.time()
        self.start()

    def update(self):
        if self.active and self.last_jump_time:
            if time.time() - self.last_jump_time > self.stop_delay:
                self.total_time += time.time() - self.session_start
                self.active = False
                self.session_start = None

    def get_time(self):
        if self.active:
            return self.total_time + (time.time() - self.session_start)
        return self.total_time