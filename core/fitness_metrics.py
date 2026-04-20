class FitnessMetrics:
    def __init__(self, weight):
        self.weight = weight
        self.jump_times = []

    def add_jump(self):
        import time
        self.jump_times.append(time.time())

    def rpm(self):
        import time
        now = time.time()
        self.jump_times = [t for t in self.jump_times if now - t <= 60]
        return len(self.jump_times)

    def calories(self, duration):
        return 0.0175 * 12 * self.weight * (duration / 60)