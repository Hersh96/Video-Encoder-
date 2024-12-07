import json
import numpy as np
from huffman_coder import HuffmanCoder
from dct_utils import process_frame_dct, reconstruct_frame_dct
from image_processor import ImageProcessor
from video_writer import CustomVideoWriter
from video_effects import VideoEffects

class VideoEncoder:
    def __init__(self, input_folder, output_path, resolution, framerate=10, verbose=False):
        self.input_folder = input_folder
        self.output_path = output_path
        self.width, self.height = resolution
        self.framerate = framerate
        self.verbose = verbose

    def encode_video(self, quant_factor=50.0, effect="none"):
        writer = CustomVideoWriter(self.output_path, (self.width, self.height), self.framerate, self.verbose)
        if self.input_folder is None:
            raise ValueError("Input folder not specified for encoding.")

        processor = ImageProcessor(self.input_folder, self.width, self.height, self.verbose)
        frame_count = 0
        for frame in processor.process_images():
            if effect != "none":
                frame = VideoEffects.apply_custom_effect(frame, effect)

            channels_data, shape = process_frame_dct(frame, block_size=8, quant_factor=quant_factor)
            combined_data = [item for ch in channels_data for item in ch]

            huffman_result = HuffmanCoder.compress(combined_data)
            frame_info = {
                "encoded_data": huffman_result["encoded_data"],
                "codes": huffman_result["codes"],
                "shape": shape,
                "channel_lengths": [len(ch) for ch in channels_data]
            }
            encoded_frame = json.dumps(frame_info)
            writer.write_frame(encoded_frame)
            frame_count += 1

        writer.save()
        if self.verbose:
            print(f"Encoding complete. {frame_count} frames processed.")

    def decode_video(self, effect="none"):
        metadata, frames = CustomVideoWriter.load(self.output_path, verbose=self.verbose)

        decoded_frames = []
        for frame_data in frames:
            frame_info = json.loads(frame_data)
            encoded_data = frame_info["encoded_data"]
            codes = frame_info["codes"]
            shape = tuple(frame_info["shape"])
            channel_lengths = frame_info["channel_lengths"]

            decoded_symbols = HuffmanCoder.decompress(encoded_data, codes)
            decoded_symbols = [int(x) for x in decoded_symbols]

            c1_len, c2_len, c3_len = channel_lengths
            c1 = decoded_symbols[:c1_len]
            c2 = decoded_symbols[c1_len:c1_len+c2_len]
            c3 = decoded_symbols[c1_len+c2_len:]
            channels = [c1, c2, c3]

            frame = reconstruct_frame_dct(channels, shape, block_size=8, quant_factor=50.0)

            if effect != "none":
                frame = VideoEffects.apply_custom_effect(frame, effect)

            decoded_frames.append(frame)

        return decoded_frames
