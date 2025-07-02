# Development Workflow

## Quick Start

### 1. Development Mode (Watch + Hot Reload)
```bash
npm run dev
```
- Starts development server with hot reload
- Watches for changes in `src/` and `assets/` folders
- Automatically opens browser
- Assets are copied to `dist/assets/` automatically

### 2. Production Build
```bash
npm run build
```
- Creates optimized production build in `dist/` folder
- Minifies code and assets
- Ready for deployment

## SpriteBuilder Integration

### Step 1: Generate Sprites
1. Place your `.mp4` videos in `SpriteBuilder/input/`
2. Run: `SpriteBuilder/run_force_rebuild.bat`
3. Find generated sprites in `SpriteBuilder/output/`

### Step 2: Add to Game
1. Copy sprites from `SpriteBuilder/output/` to `assets/`
2. Update your Phaser code to load the sprites:

```javascript
// In preload function
this.load.spritesheet('player', 'assets/player.png', {
    frameWidth: 64,
    frameHeight: 64
});

// In create function
this.player = this.add.sprite(400, 300, 'player');
```

## File Structure

```
odinclicker/
├── src/
│   ├── index.js          # Main game entry point
│   └── index.html        # HTML template
├── assets/               # Game assets (sprites, sounds, etc.)
├── dist/                 # Built game (generated)
├── SpriteBuilder/        # Sprite generation tool
└── package.json          # Dependencies and scripts
```

## Available Scripts

- `npm start` - Development server (one-time)
- `npm run dev` - Development server with watch mode
- `npm run build` - Production build
- `npm run build:dev` - Development build with watch mode

## Asset Management

- **Images:** Place in `assets/` folder
- **Sprite Sheets:** Copy both `.png` and `.json` files
- **Audio:** Supported formats: `.mp3`, `.wav`, `.ogg`
- **Video:** Supported formats: `.mp4`, `.webm`

## Tips

1. **Hot Reload:** Changes to `src/` files will automatically reload the game
2. **Asset Updates:** Changes to `assets/` will trigger a page refresh
3. **SpriteBuilder:** Always use the batch files to ensure virtual environment is activated
4. **Performance:** Large spritesheets may cause warnings - consider optimizing image sizes