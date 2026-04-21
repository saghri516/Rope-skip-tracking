import cv2
import time

from core.detector import PoseDetector
from utils.timer import WorkoutTimer
from utils.saver import save_session
from config import threshold, stop_delay, user_weight

detector = PoseDetector()
timer = WorkoutTimer(stop_delay=stop_delay)

prev_y = None
jump_count = 0
state = "down"

workout_active = False
last_jump_time = None

cap = cv2.VideoCapture(0)

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    result = detector.process(frame)

    if result.pose_landmarks:
        detector.draw(frame, result.pose_landmarks)

        hip = detector.get_hip(result.pose_landmarks)

        if hip:
            h, w, _ = frame.shape
            cx, cy = int(hip[0] * w), int(hip[1] * h)

            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            if prev_y is not None:
                diff = prev_y - cy

                if diff > threshold:
                    state = "up"

                elif diff < -threshold and state == "up":
                    state = "down"
                    jump_count += 1

                    timer.mark_activity()
                    last_jump_time = time.time()

                    if not workout_active:
                        workout_active = True

            prev_y = cy

    timer.update()
    current_time = timer.get_time()

    if workout_active and last_jump_time is not None:
        if time.time() - last_jump_time > stop_delay:

            duration = timer.get_time()

            calories = 0.0175 * 12 * user_weight * (duration / 60)

            save_session(jump_count, duration, calories)

            workout_active = False
            last_jump_time = None

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time + 0.00001)
    prev_time = curr_time

    cv2.putText(frame, f"Jumps: {jump_count}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Time: {current_time:.1f}s", (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Smart Rope Fitness Tracker PRO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        # ✅ SAVE LAST SESSION ON EXIT
        if workout_active:
            duration = timer.get_time()
            calories = 0.0175 * 12 * user_weight * (duration / 60)

            save_session(jump_count, duration, calories)

            break

cap.release()
cv2.destroyAllWindows()