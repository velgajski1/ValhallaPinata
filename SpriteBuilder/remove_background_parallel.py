import os
import glob
from multiprocessing import Pool, cpu_count
from rembg import remove
from PIL import Image
from tqdm import tqdm  # Progress bar

def process_frame(frame_path):
    out_path = frame_path.replace(".png", "_no_bg.png")
    try:
        with open(frame_path, 'rb') as i:
            input_data = i.read()
            output_data = remove(input_data, only_mask=False)
            with open(out_path, 'wb') as o:
                o.write(output_data)
        return f"✅ {os.path.basename(frame_path)}"
    except Exception as e:
        return f"❌ {frame_path}: {e}"

def cleanup_original_files(input_folder):
    """Remove original PNG files after background removal is complete"""
    original_files = glob.glob(os.path.join(input_folder, "*.png"))
    # Filter out _no_bg.png files, keep only original files
    original_files = [f for f in original_files if not f.endswith("_no_bg.png")]

    if original_files:
        print(f"🧹 Cleaning up {len(original_files)} original files...")
        for file_path in original_files:
            try:
                os.remove(file_path)
                print(f"  ✅ Removed: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"  ⚠️  Could not remove {os.path.basename(file_path)}: {e}")
    else:
        print("🧹 No original files to clean up")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python remove_background_parallel.py tmp/your_video_folder")
        exit(1)

    input_folder = sys.argv[1]
    frames = sorted(glob.glob(os.path.join(input_folder, "*.png")))

    print(f"Found {len(frames)} frames to process...")

    if not frames:
        exit(0)

    # Warm up with first frame to cache model
    print(f"📥 Warming up with {frames[0]} to cache model...")
    print(process_frame(frames[0]))
    frames = frames[1:]

    # Use multiprocessing with tqdm progress bar
    if frames:
        with Pool(processes=min(cpu_count(), 8)) as pool:
            for result in tqdm(pool.imap(process_frame, frames), total=len(frames), desc="🧠 Removing backgrounds"):
                pass

    # Clean up original files after successful processing
    cleanup_original_files(input_folder)

    print("🎉 All frames processed with background removed.")
