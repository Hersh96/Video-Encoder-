import json
import struct
import os

class CustomVideoWriter:
    def __init__(self, output_path, resolution, framerate=10, verbose=False):
        self.output_path = output_path
        self.width, self.height = resolution
        self.framerate = framerate
        self.verbose = verbose
        self.frames = []

    def write_frame(self, encoded_frame):
        self.frames.append(encoded_frame)

    def save(self):
        metadata = {
            "resolution": (self.width, self.height),
            "framerate": self.framerate,
            "frames_count": len(self.frames),
        }

        with open(self.output_path, "wb") as f:
            metadata_bytes = json.dumps(metadata).encode("utf-8")
            f.write(struct.pack("I", len(metadata_bytes)))
            f.write(metadata_bytes)

            for frame in self.frames:
                frame_data = frame.encode("utf-8")
                frame_length = len(frame_data)
                f.write(struct.pack("I", frame_length))
                f.write(frame_data)

        if self.verbose:
            print(f"Custom video saved to {self.output_path}")

    @staticmethod
    def load(input_path, verbose=False):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"{input_path} does not exist.")

        with open(input_path, "rb") as f:
            metadata_length = struct.unpack("I", f.read(4))[0]
            metadata_bytes = f.read(metadata_length)
            metadata = json.loads(metadata_bytes.decode("utf-8"))

            if verbose:
                print(f"Loaded metadata: {metadata}")

            frames = []
            while True:
                size_data = f.read(4)
                if not size_data:
                    break
                frame_length = struct.unpack("I", size_data)[0]
                frame_data = f.read(frame_length).decode("utf-8")
                frames.append(frame_data)

        return metadata, frames
