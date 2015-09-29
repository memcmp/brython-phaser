from browser import window
import random


class Game(object):

    def __init__(self):
        window.console.log("game-init")
        self.game = window.Phaser.Game(
            800,
            600,
            window.Phaser.AUTO,
            '',
            {"preload": self.preload,
             "create": self.create,
             "update": self.update})
        self.game = self.game
        self.score = 0

    def preload(self):
        window.console.log('game-preload')
        self.game.load.image('sky', 'assets/sky.png')
        self.game.load.image('ground', 'assets/platform.png')
        self.game.load.image('star', 'assets/star.png')
        self.game.load.spritesheet('dude', 'assets/dude.png', 32, 48)

    def create(self):
        window.console.log('game-create')

        self.game.physics.startSystem(window.Phaser.Physics.ARCADE)

        self.game.add.sprite(0, 0, 'sky')

        self.platforms = self.game.add.group()
        self.platforms.enableBody = True

        ground = self.platforms.create(0, self.game.world.height - 64, 'ground')
        ground.scale.setTo(2, 2)
        ground.body.immovable = True

        ledge = self.platforms.create(400, 400, 'ground')
        ledge.body.immovable = True

        ledge = self.platforms.create(-150, 200, 'ground')
        ledge.body.immovable = True

        self.player = self.game.add.sprite(32, self.game.world.height - 150, 'dude')
        self.game.physics.arcade.enable(self.player)

        self.player.body.bounce.y = 0.2
        self.player.body.gravity.y = 300
        self.player.body.collideWorldBounds = True

        self.player.animations.add('left', [0, 1, 2, 3], 10, True)
        self.player.animations.add('right', [5, 6, 7, 8], 10, True)

        self.cursors = self.game.input.keyboard.createCursorKeys()

        self.stars = self.game.add.group()
        self.stars.enableBody = True
        for i in range(0, 12):
            star = self.stars.create(i * 70, 150, 'star')
            star.body.gravity.y = 6
            star.body.bounce.y = 0.7 + random.random() * 0.2

        self.score = 0
        self.scoreText = self.game.add.text(16, 16, 'score: 0')

    def collectStar(self, player, star):
        self.stars.remove(star)
        self.score += 10
        self.scoreText.setText('score: {}'.format(self.score))

    def update(self):
        self.game.physics.arcade.collide(self.player, self.platforms)
        self.game.physics.arcade.collide(self.stars, self.platforms)
        self.game.physics.arcade.overlap(self.player, self.stars, self.collectStar, None, self)

        self.player.body.velocity.x = 0
        if self.cursors.left.isDown:
            self.player.body.velocity.x = - 150
            self.player.animations.play('left')
        elif self.cursors.right.isDown:
            self.player.body.velocity.x = 150
            self.player.animations.play('right')
        else:
            self.player.animations.stop()
            self.player.frame = 4

        if self.cursors.up.isDown and self.player.body.touching.down:
            self.player.body.velocity.y = -350


GAME = Game()
