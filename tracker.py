import cv2
import mediapipe as mp


class EyeTracker:
    def __init__(self):
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,  # enables iris landmarks
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_gaze_point(self, frame, screen_w, screen_h):
        # Convert BGR (OpenCV) to RGB (MediaPipe requirement)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_points = results.multi_face_landmarks[0].landmark

            # Left iris landmark (468)
            left_iris = mesh_points[468]

            x = int(left_iris.x * screen_w)
            y = int(left_iris.y * screen_h)

            return x, y

        return None
