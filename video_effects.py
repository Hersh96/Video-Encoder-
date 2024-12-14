import cv2
import numpy as np

class VideoEffects:
    @staticmethod
    def apply_grayscale(frame):
        # Convert to grayscale and back to 3 channels
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def apply_sepia(frame):
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        frame_sepia = cv2.transform(frame, sepia_filter)
        return np.clip(frame_sepia, 0, 255).astype(np.uint8)

    @staticmethod
    def apply_negative(frame):
        return 255 - frame

    @staticmethod
    def apply_edge_detection(frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_frame, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def apply_custom_effect(frame, effect_name):
        if effect_name == "grayscale":
            return VideoEffects.apply_grayscale(frame)
        elif effect_name == "sepia":
            return VideoEffects.apply_sepia(frame)
        elif effect_name == "negative":
            return VideoEffects.apply_negative(frame)
        elif effect_name == "edge":
            return VideoEffects.apply_edge_detection(frame)
        else:
            return frame  # "none"
