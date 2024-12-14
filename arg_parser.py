import argparse
import os

def parse_resolution(value):
    try:
        width, height = map(int, value.lower().split('x'))
        return (width, height)
    except ValueError:
        raise argparse.ArgumentTypeError("Resolution must be in WIDTHxHEIGHT format, e.g., 640x480.")

class CLIArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Convert a sequence of images into a DCT+Huffman encoded video."
        )
        self._add_arguments()
        self.args = self.parser.parse_args()
        self._validate_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            'command',
            choices=['encode', 'view'],
            help='Command to execute: encode images or view the decoded video.'
        )

        self.parser.add_argument(
            'input_folder',
            type=str,
            nargs='?',
            help='Path to the folder containing input images (required for encode).'
        )

        self.parser.add_argument(
            '-o', '--output',
            type=str,
            default='output_custom.bin',
            help='Name of the output compressed file (default: output_custom.bin).'
        )

        self.parser.add_argument(
            '-fr', '--framerate',
            type=int,
            default=10,
            help='Frame rate for playback and output (default: 10).'
        )

        self.parser.add_argument(
            '-r', '--resolution',
            type=parse_resolution,
            default=(320, 240),
            metavar='WIDTHxHEIGHT',
            help='Resolution of the frames (e.g., 320x240). Default is 320x240.'
        )

        self.parser.add_argument(
            '-e', '--effect',
            type=str,
            choices=['none', 'grayscale', 'sepia', 'negative', 'edge'],
            default='none',
            help='Apply a special effect to the video: none, grayscale, sepia, negative, edge.'
        )

        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output.'
        )

    def _validate_arguments(self):
        if self.args.command == 'encode':
            if not self.args.input_folder:
                self.parser.error("Input folder is required for encoding.")
            if not os.path.isdir(self.args.input_folder):
                self.parser.error(f"The folder '{self.args.input_folder}' does not exist.")

    def get_args(self):
        return self.args
