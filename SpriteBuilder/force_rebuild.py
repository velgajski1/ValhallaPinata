import os
import sys
import subprocess
import glob
import shutil

TMP_FOLDER = 'tmp'
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
REMOVE_BG_SCRIPT = 'remove_background_parallel.py'
BUILD_SCRIPT = 'build_sprite.bat'

def shorten_filename(filename, max_length=20):
    """Shorten filename to max_length characters, preserving extension"""
    name, ext = os.path.splitext(filename)
    if len(name) <= max_length:
        return filename

    # Shorten name and add extension
    shortened_name = name[:max_length]
    return shortened_name + ext

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

def process_video(video_path):
    """Process a single video file"""
    folder_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_path = os.path.join(TMP_FOLDER, folder_name)

    print(f"\n🎬 Processing: {os.path.basename(video_path)}")
    print("=" * 50)

    # Extract frames from video
    if not extract_frames(video_path):
        print(f"❌ Failed to extract frames from {os.path.basename(video_path)}")
        return False

    frames = [f for f in os.listdir(frame_path) if f.endswith('.png') and not f.endswith('_no_bg.png')]
    if not frames:
        print(f'❌ No PNG frames found in {frame_path}.')
        return False

    print(f'🧹 Removing backgrounds for frames in {frame_path}...')
    result = subprocess.run([sys.executable, REMOVE_BG_SCRIPT, frame_path])
    if result.returncode != 0:
        print('❌ Background removal failed.')
        return False

    print(f'✅ Complete: {folder_name}')
    return True

def process_all_videos():
    """Process all .mp4 files in the input folder"""
    video_files = glob.glob(os.path.join(INPUT_FOLDER, "*.mp4"))

    if not video_files:
        print(f"❌ No .mp4 files found in {INPUT_FOLDER} folder")
        return

    print(f"🎬 Found {len(video_files)} video(s) to process:")
    for video in video_files:
        original_name = os.path.basename(video)
        shortened_name = shorten_filename(original_name, 20)
        if original_name != shortened_name:
            print(f"  - {original_name} → {shortened_name}")
        else:
            print(f"  - {original_name}")

    print(f"\n🧹 Cleaning entire tmp folder...")
    if os.path.exists(TMP_FOLDER):
        try:
            shutil.rmtree(TMP_FOLDER)
            print(f"  ✅ Removed: {TMP_FOLDER}")
        except Exception as e:
            print(f"  ⚠️  Could not remove {TMP_FOLDER}: {e}")

    # Recreate tmp folder
    os.makedirs(TMP_FOLDER, exist_ok=True)
    print(f"  ✅ Recreated: {TMP_FOLDER}")

    print(f"\n🚀 Starting batch processing...")

    success_count = 0
    for video_file in video_files:
        if process_video(video_file):
            success_count += 1

    print(f"\n🎉 Batch processing complete: {success_count}/{len(video_files)} videos processed successfully")

def main():
    if len(sys.argv) == 1:
        # No arguments - process all videos in input folder
        process_all_videos()
        return

    if len(sys.argv) != 2:
        print('Usage: python force_rebuild.py [video_file_or_folder_name]')
        print('Examples:')
        print('  python force_rebuild.py                    # Process all videos in input/')
        print('  python force_rebuild.py my_video.mp4       # Process specific video')
        print('  python force_rebuild.py my_video_folder    # Process existing folder')
        sys.exit(1)

    input_arg = sys.argv[1]

    # Check if it's a video file
    if input_arg.lower().endswith('.mp4'):
        video_path = os.path.join(INPUT_FOLDER, input_arg)
        if not os.path.exists(video_path):
            print(f'❌ Video file not found: {video_path}')
            sys.exit(1)

        process_video(video_path)
    else:
        # Assume it's a folder name
        folder = input_arg
        frame_path = os.path.join(TMP_FOLDER, folder)
        if not os.path.isdir(frame_path):
            print(f'❌ Temp folder not found: {frame_path}')
            sys.exit(1)

        frames = [f for f in os.listdir(frame_path) if f.endswith('.png') and not f.endswith('_no_bg.png')]
        if not frames:
            print(f'❌ No PNG frames found in {frame_path}.')
            sys.exit(1)

        print(f'🧹 Removing backgrounds for frames in {frame_path}...')
        result = subprocess.run([sys.executable, REMOVE_BG_SCRIPT, frame_path])
        if result.returncode != 0:
            print('❌ Background removal failed.')
            sys.exit(1)

        print(f'✅ Force rebuild complete for {folder}.')

    # CLEANUP: Delete everything in output and tmp folders
    def clean_folder(folder):
        for entry in os.listdir(folder):
            path = os.path.join(folder, entry)
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    print("\n🧹 Cleaning up output and tmp folders...")
    clean_folder("output")
    clean_folder("tmp")
    print("✅ All files in output/ and tmp/ have been deleted.")

if __name__ == '__main__':
    if not check_dependencies():
        sys.exit(1)
    main()