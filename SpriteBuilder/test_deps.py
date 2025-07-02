#!/usr/bin/env python3

try:
    import onnxruntime
    print(f"✅ onnxruntime version: {onnxruntime.__version__}")
except ImportError:
    print("❌ onnxruntime not found")

try:
    import rembg
    print(f"✅ rembg version: {rembg.__version__}")
except ImportError:
    print("❌ rembg not found")

try:
    import PIL
    print(f"✅ Pillow version: {PIL.__version__}")
except ImportError:
    print("❌ Pillow not found")

try:
    import tqdm
    print(f"✅ tqdm version: {tqdm.__version__}")
except ImportError:
    print("❌ tqdm not found")

try:
    import subprocess
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ ffmpeg available")
    else:
        print("❌ ffmpeg not found")
except FileNotFoundError:
    print("❌ ffmpeg not found")