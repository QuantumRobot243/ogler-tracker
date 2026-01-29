import cv2
import dlib
import numpy as np

class EyeTracker:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def get_gaze_point(self, frame, screen_w, screen_h):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)

            x_pts = [landmarks.part(i).x for i in range(36, 42)]
            y_pts = [landmarks.part(i).y for i in range(36, 42)]

            center_x = sum(x_pts) / len(x_pts)
            center_y = sum(y_pts) / len(y_pts)

            cam_h, cam_w = frame.shape[:2]

            screen_x = int((center_x / cam_w) * screen_w)
            screen_y = int((center_y / cam_h) * screen_h)

            return screen_x, screen_y

        return None
