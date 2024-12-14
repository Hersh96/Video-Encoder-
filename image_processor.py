import cv2
import os
import glob

class ImageProcessor:
    def __init__(self, input_folder, width=320, height=240, verbose=False):
        self.input_folder = input_folder
        self.width = width
        self.height = height
        self.verbose = verbose

    def process_images(self):
        images = glob.glob(os.path.join(self.input_folder, '*.jpg'))
        images.sort()

        if len(images) == 0:
            print("No images found in the specified folder.")
            return

        if self.verbose:
            print(f"Found {len(images)} image(s).")

        for idx, image_path in enumerate(images):
            frame = cv2.imread(image_path)
            if frame is None:
                if self.verbose:
                    print(f"Warning: Unable to read '{image_path}'. Skipping.")
                continue
            frame = cv2.resize(frame, (self.width, self.height))
            if self.verbose and idx % 10 == 0:
                print(f"Processing image {idx + 1}/{len(images)}")
            yield frame
