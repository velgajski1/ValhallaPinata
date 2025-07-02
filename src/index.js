import Phaser from 'phaser';

class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameScene' });
    this.swingTime = 0;
    this.dialogueString = ''; // The text content
    this.currentCharIndex = 0;
    this.isTyping = false;
    this.typeSpeed = 50; // milliseconds per character
    this.dialogueTextObject = null; // The Phaser text object
    this.odin = null;
    this.pinata = null;
    this.pinataSwing = null;
    this.speechBox = null;
    this.timerText = null;
    this.scoreText = null;
    this.gameStarted = false;
    this.timeRemaining = 10; // 10 seconds
    this.score = 0; // Score counter
    this.dialogueEvent = null; // Store dialogue event reference
    this.timerEvent = null; // Store timer event reference
  }

  preload() {
    // Load background image
    this.load.image('background', 'assets/bg.jpg');

    // Load pinata image (PNG)
    this.load.image('pinata', 'assets/pinata.png');

    // Load spritesheet and atlas
    this.load.atlas('odin', 'assets/spritesheet/main.png', 'assets/spritesheet/main.json');
  }

  create() {
    this.setupBackground();
    this.setupPinata();
    this.setupOdin();
    this.setupSpeechBox();
    this.setupTimer();
    this.setupScore();
    this.startDialogue("Welcome to Valhalla Pinata! Hit it as many times you can in 10 seconds.");
  }

  setupBackground() {
    const gameWidth = this.cameras.main.width;
    const gameHeight = this.cameras.main.height;

    this.add.image(gameWidth / 2, gameHeight / 2, 'background')
      .setDisplaySize(gameWidth, gameHeight);
  }

  setupPinata() {
    const gameWidth = this.cameras.main.width;

    this.pinata = this.add.image(gameWidth / 2, 0, 'pinata');
    this.pinata.setOrigin(0.5, 0);
    this.pinata.setScale(0.6);
    this.pinataSwing = this.pinata;

    // Make pinata clickable
    this.pinata.setInteractive();
    this.pinata.on('pointerdown', this.onPinataClick, this);
  }

  setupOdin() {
    const gameWidth = this.cameras.main.width;
    const gameHeight = this.cameras.main.height;

    this.odin = this.add.sprite(gameWidth * 0.15, gameHeight - 100, 'odin');
    this.odin.setScale(1.5);

    // Create animation from the spritesheet
    const frameNames = this.anims.generateFrameNames('odin', {
      prefix: 'odin/odin_',
      suffix: '_no_bg.png',
      start: 0,
      end: 120,
      zeroPad: 3
    });

    // Create the animation
    this.anims.create({
      key: 'odin_animation',
      frames: frameNames,
      frameRate: 12,
      repeat: -1
    });
  }

  setupSpeechBox() {
    const gameWidth = this.cameras.main.width;
    const gameHeight = this.cameras.main.height;

    const speechBoxWidth = gameWidth * 0.6;
    const speechBoxHeight = 120;
    const speechBoxX = gameWidth * 0.55;
    const speechBoxY = gameHeight * 0.85;

    // Speech box background
    this.speechBox = this.add.graphics();
    this.speechBox.fillStyle(0x000000, 0.8);
    this.speechBox.fillRoundedRect(
      speechBoxX - speechBoxWidth / 2,
      speechBoxY - speechBoxHeight / 2,
      speechBoxWidth,
      speechBoxHeight,
      10
    );
    this.speechBox.lineStyle(3, 0xffffff, 1);
    this.speechBox.strokeRoundedRect(
      speechBoxX - speechBoxWidth / 2,
      speechBoxY - speechBoxHeight / 2,
      speechBoxWidth,
      speechBoxHeight,
      10
    );

    // Text display
    this.dialogueTextObject = this.add.text(
      speechBoxX - speechBoxWidth / 2 + 20,
      speechBoxY - speechBoxHeight / 2 + 20,
      '',
      {
        fontSize: '24px',
        color: '#ffffff',
        wordWrap: { width: speechBoxWidth - 40 },
        lineSpacing: 5
      }
    );
  }

  setupTimer() {
    const gameWidth = this.cameras.main.width;
    const gameHeight = this.cameras.main.height;

    // Create big timer text in the center
    this.timerText = this.add.text(
      gameWidth / 2,
      gameHeight * 0.5 + 70, // Moved down 70px
      '10',
      {
        fontSize: '180px', // Made larger
        color: '#ffffff',
        fontStyle: 'bold',
        stroke: '#000000',
        strokeThickness: 4
      }
    );
    this.timerText.setOrigin(0.5);
    this.timerText.setVisible(false); // Start invisible
  }

  setupScore() {
    // Create score text in top left
    this.scoreText = this.add.text(
      20,
      20,
      'Score: 0',
      {
        fontSize: '32px',
        color: '#ffffff',
        fontStyle: 'bold',
        stroke: '#000000',
        strokeThickness: 2
      }
    );
    this.scoreText.setOrigin(0, 0); // Anchor to top left
  }

  onPinataClick() {
    // Don't allow clicking if game is over
    if (this.timeRemaining <= 0) {
      return;
    }

    if (!this.gameStarted) {
      this.gameStarted = true;
      this.timerText.setVisible(true);
      this.startTimer();
    }

    // Increment score on every click
    this.score++;
    this.scoreText.setText(`Score: ${this.score}`);
  }

  startTimer() {
    this.timerEvent = this.time.addEvent({
      delay: 1000, // 1 second
      callback: this.updateTimer,
      callbackScope: this,
      loop: true
    });
  }

  updateTimer() {
    this.timeRemaining--;
    this.timerText.setText(this.timeRemaining.toString());

    if (this.timeRemaining <= 0) {
      this.endGame();
    }
  }

  endGame() {
    // Stop the timer
    if (this.timerEvent) {
      this.timerEvent.remove();
    }
    this.timerText.setText('TIME\'S UP!');

    // Hide timer after 1 second and show congratulations
    this.time.delayedCall(1000, () => {
      this.timerText.setVisible(false);
      this.showCongratulations();
    });
  }

  showCongratulations() {
    // Start Odin's animation
    this.odin.play('odin_animation');

    // Show congratulations message
    this.startDialogue(`Congratulations! You have scored: ${this.score}`);
  }

  startDialogue(text) {
    this.dialogueString = text;
    this.currentCharIndex = 0;
    this.isTyping = true;
    this.dialogueTextObject.setText('');

    // Start Odin's animation during dialogue
    this.odin.play('odin_animation');

    // Start typewriter effect
    this.dialogueEvent = this.time.addEvent({
      delay: this.typeSpeed,
      callback: this.typeNextCharacter,
      callbackScope: this,
      loop: true
    });
  }

  typeNextCharacter() {
    if (this.currentCharIndex < this.dialogueString.length) {
      this.dialogueTextObject.setText(this.dialogueString.substring(0, this.currentCharIndex + 1));
      this.currentCharIndex++;
    } else {
      // Finished typing
      this.isTyping = false;

      // Remove only the dialogue event, not all events
      if (this.dialogueEvent) {
        this.dialogueEvent.remove();
      }

      // Stop Odin's animation and go to first frame
      this.odin.stop();
      this.odin.setFrame(0);
    }
  }

  update(time, delta) {
    // Make the pinata swing left and right
    if (this.pinataSwing) {
      this.swingTime += delta / 1000; // seconds
      const amplitude = 15; // max angle in degrees
      const speed = 2; // swings per second
      this.pinataSwing.angle = amplitude * Math.sin(this.swingTime * speed);
    }
  }
}

const config = {
  type: Phaser.AUTO,
  width: window.innerWidth,
  height: window.innerHeight,
  backgroundColor: '#222',
  scene: GameScene,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300 },
      debug: false
    }
  },
  scale: {
    mode: Phaser.Scale.RESIZE,
    parent: 'game-container',
    width: '100%',
    height: '100%',
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};

const game = new Phaser.Game(config);