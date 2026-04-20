import mediapipe as mp

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        rgb = frame[:, :, ::-1]  # BGR → RGB
        result = self.pose.process(rgb)
        return result

    def draw(self, frame, landmarks):
        self.mp_draw.draw_landmarks(
            frame,
            landmarks,
            self.mp_pose.POSE_CONNECTIONS
        )

    def get_hip(self, landmarks):
        if not landmarks:
            return None

        hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        return hip.x, hip.y