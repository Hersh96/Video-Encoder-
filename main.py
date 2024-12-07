import sys
from arg_parser import CLIArguments
from video_encoder import VideoEncoder
from utils import save_frames_as_video
import os
import cv2
import subprocess

def main():
    cli_args = CLIArguments()
    args = cli_args.get_args()

    if args.command == "encode":
        encoder = VideoEncoder(
            input_folder=args.input_folder,
            output_path=args.output,
            resolution=args.resolution,
            framerate=args.framerate,
            verbose=args.verbose
        )
        encoder.encode_video(effect=args.effect)

    elif args.command == "view":
        encoder = VideoEncoder(
            input_folder=None,
            output_path=args.output,
            resolution=(0,0),  # Not used
            framerate=args.framerate,
            verbose=args.verbose
        )
        frames = encoder.decode_video(effect=args.effect)
        if not frames:
            print("No frames to display.")
            return
        view_video_path = "decoded_view.avi"
        save_frames_as_video(frames, view_video_path, args.framerate)

        # Open with default media player
        if sys.platform.startswith('win'):
            os.startfile(view_video_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', view_video_path])
        else:
            subprocess.run(['xdg-open', view_video_path])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        from gui import run_gui
        run_gui()
