class JumpCounter:
    def __init__(self, threshold):
        self.threshold = threshold
        self.prev_y = None
        self.state = "down"
        self.jump_count = 0

    def update(self, cy):
        if self.prev_y is None:
            self.prev_y = cy
            return self.jump_count, False

        diff = self.prev_y - cy
        jumped = False

        if diff > self.threshold:
            self.state = "up"

        elif diff < -self.threshold and self.state == "up":
            self.state = "down"
            self.jump_count += 1
            jumped = True

        self.prev_y = cy
        return self.jump_count, jumped