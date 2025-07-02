import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading

INPUT_FOLDER = "input"
TMP_FOLDER = "tmp"
OUTPUT_FOLDER = "output"
BUILD_SCRIPT = "build_sprite.bat"

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []

    try:
        import onnxruntime
        print(f"✅ onnxruntime {onnxruntime.__version__}")
    except ImportError:
        missing_deps.append("onnxruntime")
        print("❌ onnxruntime not found")

    try:
        import rembg
        print(f"✅ rembg {rembg.__version__}")
    except ImportError:
        missing_deps.append("rembg")
        print("❌ rembg not found")

    try:
        import PIL
        print(f"✅ Pillow {PIL.__version__}")
    except ImportError:
        missing_deps.append("Pillow")
        print("❌ Pillow not found")

    try:
        import tqdm
        print(f"✅ tqdm {tqdm.__version__}")
    except ImportError:
        missing_deps.append("tqdm")
        print("❌ tqdm not found")

    # Check if ffmpeg is available
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg available")
        else:
            missing_deps.append("ffmpeg")
            print("❌ ffmpeg not found or not working")
    except FileNotFoundError:
        missing_deps.append("ffmpeg")
        print("❌ ffmpeg not found in PATH")

    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: install_requirements.bat")
        print("Or install manually: pip install onnxruntime rembg pillow tqdm")
        print("Also ensure ffmpeg is installed and in your PATH")
        return False

    print("✅ All dependencies available")
    return True

def extract_frames(video_file):
    """Extract frames from video using ffmpeg"""
    folder_name = os.path.splitext(os.path.basename(video_file))[0]
    frame_path = os.path.join(TMP_FOLDER, folder_name)

    # Create frame directory if it doesn't exist
    os.makedirs(frame_path, exist_ok=True)

    print(f"🎬 Extracting frames from: {os.path.basename(video_file)}")
    print(f"📁 Output folder: {frame_path}")

    # Extract every other frame at 1/8 size using ffmpeg
    cmd = [
        "ffmpeg", "-i", video_file,
        "-vf", "select=not(mod(n\\,2)),scale=iw/8:ih/8",  # Every other frame, 1/8 size
        "-vsync", "0",
        "-frame_pts", "1",
        os.path.join(frame_path, f"{folder_name}_%03d.png"),
        "-y"  # Overwrite existing files
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Frame extraction failed: {result.stderr}")
        return False

    # Count extracted frames
    frame_count = len([f for f in os.listdir(frame_path) if f.endswith('.png')])
    print(f"✅ Extracted {frame_count} frames to {frame_path}")
    return True

def run_build(video_file):
    folder_name = os.path.splitext(os.path.basename(video_file))[0]
    frame_path = os.path.join(TMP_FOLDER, folder_name)

    # Extract frames first
    if not extract_frames(video_file):
        print(f"❌ Failed to extract frames from {os.path.basename(video_file)}")
        return

    print(f"📸 Waiting for *_no_bg.png files in {frame_path}...")
    for _ in range(120):  # Wait up to 120s
        if any(f.endswith("_no_bg.png") for f in os.listdir(frame_path)):
            break
        time.sleep(1)
    else:
        print(f"❌ Timeout: No _no_bg.png files found in {frame_path}")
        return

    print(f"🚀 Running build_sprite.bat for: {folder_name}")
    subprocess.run([BUILD_SCRIPT, folder_name], shell=True)

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and str(event.src_path).lower().endswith('.mp4'):
            print(f"🎬 Detected new video: {os.path.basename(event.src_path)}")
            threading.Thread(target=run_build, args=(event.src_path,), daemon=True).start()

if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)

    print(f"🔍 Watching folder: {INPUT_FOLDER}")
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path=INPUT_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
