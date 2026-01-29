import cv2
import os
import random
import numpy as np
from tracker import EyeTracker
from visualizer import HeatmapVisualizer

SCREEN_RES = (1920, 1080)
IMG_FOLDER = "images"
OUT_FOLDER = "outputs"

def main():
    if not os.path.exists(OUT_FOLDER):
        os.makedirs(OUT_FOLDER)
        print("My Senpai told me to collect Proof ")

    all_images = [
        f for f in os.listdir(IMG_FOLDER)
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]
    if not all_images:
        print(" senpai is working so hard he is collecting images for you perv")
        return

    chosen_img_name = random.choice(all_images)
    img_path = os.path.join(IMG_FOLDER, chosen_img_name)
    base_img = cv2.imread(img_path)

    if base_img is None:
        print(f" I need to inform to senpai that this image is not working: {img_path}")
        return

    base_img = cv2.resize(base_img, SCREEN_RES)

    tracker = EyeTracker()
    viz = HeatmapVisualizer(SCREEN_RES[0], SCREEN_RES[1])

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("Tracking...", cv2.WND_PROP_FULLSCREEN)

    print(
        f" Ara~ ara~ Kimoi is staring at {chosen_img_name}...\n"
        "Kimoi press q to stop,"
    )

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("camera-kun where are you..??")
            break

        frame = cv2.flip(frame, 1)

        gaze_point = tracker.get_gaze_point(
            frame, SCREEN_RES[0], SCREEN_RES[1]
        )

        display_img = base_img.copy()

        if gaze_point:
            viz.add_hit(gaze_point[0], gaze_point[1])
            cv2.circle(display_img, gaze_point, 10, (0, 255, 0), -1)

        cv2.imshow("Tracking...", display_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Offfff...!!!! Finaly")
            break

    print("Creep i have proff")
    final_result = viz.generate_final_overlay(base_img)

    save_path = os.path.abspath(os.path.join(
        OUT_FOLDER, f"heatmap_{chosen_img_name}"
    ))
    
    cv2.imwrite(save_path, final_result)

    print(f" Ara~ ara~ Creep, I have your secret here:\n  {save_path}")

    cap.release()
    cv2.destroyAllWindows()
    print("Go away creep...!!!")

if __name__ == "__main__":
    main()