import cv2

def save_frames_as_video(frames, output_file, framerate):
    if not frames:
        print("No frames to save.")
        return
    height, width, _ = frames[0].shape
    # Use mp4v codec for .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, framerate, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"Decoded video saved to {output_file}")
