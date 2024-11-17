import subprocess
import os

# YouTube Stream Key and Main RTMP URL
YOUTUBE_STREAM_KEY = "xr9t-k4g8-y5vd-us8z-ffz3"
YOUTUBE_RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}"
YOUTUBE_BACKUP_RTMP_URL = f"rtmp://b.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}?backup=1"

# Video URL and File
VIDEO_URL = "https://www.tikwm.com/video/media/hdplay/7418068913059269894.mp4"
VIDEO_FILE = "A.mp4"

def download_video():
    """Download the video using wget."""
    if os.path.exists(VIDEO_FILE):
        print(f"{VIDEO_FILE} already exists. Skipping download.")
    else:
        print(f"Downloading video from {VIDEO_URL}...")
        try:
            subprocess.run(["wget", "-O", VIDEO_FILE, VIDEO_URL], check=True)
            print(f"Video downloaded as {VIDEO_FILE}.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}")
            raise

def stream_video():
    """Stream the video using FFmpeg."""
    ffmpeg_command = [
        "ffmpeg",
        "-re",  # Real-time streaming
        "-stream_loop", "-1",  # Loop video indefinitely
        "-i", VIDEO_FILE,  # Input file
        "-vf", "scale=3840:2160",  # Scale to 4K resolution
        "-c:v", "libx264",  # H.264 encoder
        "-preset", "fast",  # Use "fast" for better performance
        "-b:v", "25000k",  # Video bitrate
        "-maxrate", "25000k",  # Max video bitrate
        "-bufsize", "50000k",  # Buffer size (2x bitrate)
        "-pix_fmt", "yuv420p",  # Pixel format
        "-g", "120",  # Keyframe interval (2 seconds for 60 FPS)
        "-c:a", "aac",  # Audio codec
        "-b:a", "192k",  # Audio bitrate
        "-ar", "44100",  # Audio sample rate
        "-f", "flv",  # RTMP format
        YOUTUBE_RTMP_URL  # Destination RTMP URL
    ]

    try:
        print("Starting stream on main RTMP URL...")
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError:
        print("Main RTMP URL failed, switching to backup URL...")
        ffmpeg_command[-1] = YOUTUBE_BACKUP_RTMP_URL
        try:
            subprocess.run(ffmpeg_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Streaming failed on both URLs: {e}")
            raise

def main():
    """Main function to download and stream the video."""
    while True:
        try:
            download_video()
            stream_video()
        except Exception as e:
            print(f"Error occurred: {e}. Restarting process...")
        print("Streaming completed or interrupted. Restarting...")

if __name__ == "__main__":
    main()
