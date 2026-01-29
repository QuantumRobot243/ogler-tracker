import cv2
import numpy as np


class HeatmapVisualizer:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.hitmap = np.zeros((self.h, self.w), dtype=np.float32)

    def add_hit(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            cv2.circle(self.hitmap, (x, y), 25, 1, -1)

    def generate_final_overlay(self, original_image):
        blurred = cv2.GaussianBlur(self.hitmap, (151, 151), 0)
        norm_map = cv2.normalize(
            blurred, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
        )
        color_heatmap = cv2.applyColorMap(norm_map, cv2.COLORMAP_JET)
        output = cv2.addWeighted(original_image, 0.6, color_heatmap, 0.4, 0)
        return output
