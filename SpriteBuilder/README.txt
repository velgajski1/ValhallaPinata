📦 SpriteBuilder - Automated Sprite Sheet Generator
==================================================

This tool turns any .mp4 video dropped into the 'input/' folder into a sprite sheet and optional GIF preview.

✅ Features:
- Extracts every other frame from video
- Resizes frames to 50%
- Removes background using AI (rembg)
- Packs frames into a sprite sheet (TexturePacker)
- Generates .gif preview animation
- Unity-compatible output (.png + .json)

📁 Folder Structure:
--------------------
input/      → Drop .mp4 videos here
tmp/        → Temporary working directory (auto-created)
output/     → Final sprite sheet (.png), data (.json), and preview (.gif)

🚀 How To Use:
--------------
1. Put your `.mp4` video into the `input/` folder.

2. Open Command Prompt and run:

   Manual build:
   > build_sprite.bat your_file_name

   Example:
   > build_sprite.bat bunny_jump

   OR run auto-watch mode:
   > python watch_and_build.py

3. Find your results in the `output/` folder.

🛠️ Requirements:
----------------
- Windows 10 or later
- FFmpeg (in PATH): https://ffmpeg.org/download.html
- TexturePacker (in PATH): https://www.codeandweb.com/texturepacker/download
- Python 3.7+ (with pip): https://www.python.org/downloads/windows/

📦 Python Dependencies:
-----------------------
Run the install script:
> install_requirements.bat

Or install manually:
> pip install rembg onnxruntime watchdog

🤖 Notes:
---------
- If you have `rembg.exe` (standalone), it will be used automatically.
- The script supports both `rembg` installed via pip or as a standalone .exe.
- Works best with videos that have a solid background color.

🎮 Unity Integration:
---------------------
- Copy output .png and .json into `Assets/Sprites/`
- Use Unity Sprite Editor or a TexturePacker importer to slice them
- You can automate this further using Unity Editor scripts

Enjoy!
