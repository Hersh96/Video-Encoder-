import subprocess

class AudioIntegrator:
    @staticmethod
    def add_audio_to_video(video_file, audio_file, output_file):
        try:
            command = [
                "ffmpeg",
                "-y",
                "-i", video_file,
                "-i", audio_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-strict", "experimental",
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"Audio added successfully. Saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error integrating audio: {e}")
