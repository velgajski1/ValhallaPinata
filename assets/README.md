# Assets Folder

This folder contains all game assets (sprites, sounds, etc.) for your Phaser 3 game.

## SpriteBuilder Integration

1. **Generate sprites with SpriteBuilder:**
   - Place your `.mp4` videos in `SpriteBuilder/input/`
   - Run `SpriteBuilder/run_force_rebuild.bat`
   - Find output in `SpriteBuilder/output/`

2. **Copy sprites to this folder:**
   - Copy the generated `.png` and `.json` files from `SpriteBuilder/output/` to this `assets/` folder
   - The sprites will be automatically available in your Phaser game

## Asset Types

- **Images/Sprites:** `.png`, `.jpg`, `.gif`
- **Sprite Sheets:** `.png` + `.json` (TexturePacker format)
- **Audio:** `.mp3`, `.wav`, `.ogg`
- **Video:** `.mp4`, `.webm`

## Usage in Phaser

```javascript
// In your preload function:
this.load.image('sprite', 'assets/sprite.png');
this.load.spritesheet('player', 'assets/player.png', { frameWidth: 32, frameHeight: 32 });
this.load.audio('sound', 'assets/sound.mp3');

// In your create function:
this.add.image(400, 300, 'sprite');
```

## File Structure Example

```
assets/
├── sprites/
│   ├── player.png
│   ├── player.json
│   └── enemy.png
├── sounds/
│   ├── jump.mp3
│   └── collect.wav
└── backgrounds/
    └── level1.png
```