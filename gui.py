import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess
from video_encoder import VideoEncoder
from audio_integrator import AudioIntegrator
from utils import save_frames_as_video
import cv2

def run_encoding(input_folder, output_file, width, height, framerate, effect, verbose):
    try:
        encoder = VideoEncoder(
            input_folder=input_folder,
            output_path=output_file,
            resolution=(width, height),
            framerate=framerate,
            verbose=verbose
        )
        encoder.encode_video(quant_factor=50.0, effect=effect)
        messagebox.showinfo("Success", f"Encoding completed. Output: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_viewing(output_file, framerate, effect, verbose):
    try:
        encoder = VideoEncoder(None, output_file, (0,0), framerate=framerate, verbose=verbose)
        frames = encoder.decode_video(effect=effect)

        if not frames:
            messagebox.showwarning("Warning", "No frames to display.")
            return

        # Save as mp4 file before displaying
        mp4_output = "decoded_view.mp4"
        save_frames_as_video(frames, mp4_output, framerate)

        # Now display the frames in a popup window using cv2.imshow()
        for frame in frames:
            cv2.imshow("Decoded Video", frame)
            # Wait for 'q' to quit
            if cv2.waitKey(int(1000/framerate)) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_audio_integration(video_bin, audio_file, framerate):
    try:
        encoder = VideoEncoder(None, video_bin, (0,0), framerate=framerate, verbose=False)
        frames = encoder.decode_video(effect="none")
        intermediate_video = "decoded_video.avi"
        save_frames_as_video(frames, intermediate_video, framerate)

        output_with_audio = "final_output.mp4"
        AudioIntegrator.add_audio_to_video(intermediate_video, audio_file, output_with_audio)
        messagebox.showinfo("Success", f"Video with audio saved at {output_with_audio}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_gui():
    root = tk.Tk()
    root.title("DCT+Huffman Video Encoder with Effects & Audio")

    input_folder_var = tk.StringVar()
    output_file_var = tk.StringVar(value="output_custom.bin")
    effect_var = tk.StringVar(value="none")
    width_var = tk.IntVar(value=320)
    height_var = tk.IntVar(value=240)
    framerate_var = tk.IntVar(value=10)
    verbose_var = tk.BooleanVar(value=False)
    audio_file_var = tk.StringVar()

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            input_folder_var.set(folder)

    def browse_audio_file():
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file:
            audio_file_var.set(file)

    def start_encoding():
        input_folder = input_folder_var.get().strip()
        output_file = output_file_var.get().strip()
        width = width_var.get()
        height = height_var.get()
        framerate = framerate_var.get()
        effect = effect_var.get()
        verbose = verbose_var.get()

        if not input_folder or not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Please select a valid input folder.")
            return

        t = threading.Thread(target=run_encoding, args=(input_folder, output_file, width, height, framerate, effect, verbose))
        t.start()

    def start_viewing():
        output_file = output_file_var.get().strip()
        effect = effect_var.get()
        framerate = framerate_var.get()
        verbose = verbose_var.get()

        if not os.path.exists(output_file):
            messagebox.showerror("Error", f"File '{output_file}' not found.")
            return

        t = threading.Thread(target=run_viewing, args=(output_file, framerate, effect, verbose))
        t.start()

    def start_audio_integration():
        video_bin = output_file_var.get().strip()
        audio_file = audio_file_var.get().strip()
        framerate = framerate_var.get()
        if not os.path.exists(video_bin):
            messagebox.showerror("Error", f"Video file '{video_bin}' not found.")
            return
        if not audio_file or not os.path.exists(audio_file):
            messagebox.showerror("Error", "Please select a valid audio file.")
            return

        t = threading.Thread(target=run_audio_integration, args=(video_bin, audio_file, framerate))
        t.start()

    # Layout
    tk.Label(root, text="Input Folder:").grid(row=0, column=0, sticky="e")
    tk.Entry(root, textvariable=input_folder_var, width=40).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=5)

    tk.Label(root, text="Output File:").grid(row=1, column=0, sticky="e")
    tk.Entry(root, textvariable=output_file_var, width=40).grid(row=1, column=1, columnspan=2, sticky="w")

    tk.Label(root, text="Width:").grid(row=2, column=0, sticky="e")
    tk.Entry(root, textvariable=width_var, width=10).grid(row=2, column=1, sticky="w")

    tk.Label(root, text="Height:").grid(row=3, column=0, sticky="e")
    tk.Entry(root, textvariable=height_var, width=10).grid(row=3, column=1, sticky="w")

    tk.Label(root, text="Framerate:").grid(row=4, column=0, sticky="e")
    tk.Entry(root, textvariable=framerate_var, width=10).grid(row=4, column=1, sticky="w")

    tk.Label(root, text="Effect:").grid(row=5, column=0, sticky="e")
    tk.OptionMenu(root, effect_var, "none", "grayscale", "sepia", "negative", "edge").grid(row=5, column=1, sticky="w")

    tk.Checkbutton(root, text="Verbose", variable=verbose_var).grid(row=6, column=0, columnspan=2, sticky="w")

    tk.Button(root, text="Encode", command=start_encoding, fg="blue").grid(row=7, column=0, pady=10)
    tk.Button(root, text="View", command=start_viewing, fg="green").grid(row=7, column=1, pady=10)

    tk.Label(root, text="Audio File:").grid(row=8, column=0, sticky="e")
    tk.Entry(root, textvariable=audio_file_var, width=40).grid(row=8, column=1)
    tk.Button(root, text="Browse Audio", command=browse_audio_file).grid(row=8, column=2, padx=5)

    tk.Button(root, text="Integrate Audio", command=start_audio_integration, fg="purple").grid(row=9, column=0, pady=10)

    root.mainloop()
