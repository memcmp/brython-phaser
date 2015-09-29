from browser import window
from javascript import JSConstructor
import random


class Game(object):

    def __init__(self):
        window.console.log("game-init")
        Game = JSConstructor(window.Phaser.Game)
        window.br_preload = self.preload
        window.br_create = self.create
        window.game = Game(
            800,
            600,
            window.Phaser.AUTO,
            '',
            {"preload": self.preload,
             "create": self.create,
             "update": self.update})
        self.game = window.game
        self.score = 0

    def preload(self):
        window.console.log('game-preload')
        window.game.load.image('sky', 'assets/sky.png')
        window.game.load.image('ground', 'assets/platform.png')
        window.game.load.image('star', 'assets/star.png')
        window.game.load.spritesheet('dude', 'assets/dude.png', 32, 48)

    def create(self):
        window.console.log('game-create')

        window.game.physics.startSystem(window.Phaser.Physics.ARCADE)

        window.game.add.sprite(0, 0, 'sky')

        self.player = window.game.add.sprite(32, window.game.world.height - 150, 'dude')
        window.game.physics.arcade.enable(self.player)

        #  Player physics properties. Give the little guy a slight bounce.
        self.player.body.bounce.y = 0.2
        self.player.body.gravity.y = 6
        self.player.body.collideWorldBounds = True

        self.platforms = window.game.add.group()
        ground = self.platforms.create(0, window.game.world.height - 64, 'ground')

        window.game.physics.arcade.enable(ground)
        ground.scale.setTo(2, 2)
        ground.body.immovable = True

        #  Our two animations, walking left and right.
        self.player.animations.add('left', [0, 1, 2, 3], 10, True)
        self.player.animations.add('right', [5, 6, 7, 8], 10, True)

        #  Finally some self.stars to collect
        self.stars = window.game.add.group()

        #  Here we'll create 12 of them evenly spaced apart
        for i in range(0, 12):
            #  Create a star inside of the 'self.stars' group
            star = self.stars.create(i * 70, 0, 'star')
            window.game.physics.arcade.enable(star)

            #  Let gravity do its thing
            star.body.gravity.y = 6

            #  This just gives each star a slightly random bounce value
            star.body.bounce.y = 0.7 + random.random() * 0.2

        #  The score
        self.scoreText = window.game.add.text(16, 16, 'score: 0', {"fontSize": '32px', "fill": '#000'})

        #  Our controls.
        self.cursors = window.game.input.keyboard.createCursorKeys()

    def collectStar(self, player, star):
        window.console.log('collect star')
        star.kill()
        player.kill()
        self.score += 10
        self.scoreText.content = 'Score: {}'.format(self.score)

    def update(self):
        window.console.log('game-update')
        window.game.physics.arcade.collide(self.player, self.platforms)
        window.game.physics.arcade.collide(self.stars, self.platforms)
        #  Checks to see if the self.player overlaps with any of the self.stars, if he does call the collectStar function
        window.game.physics.arcade.overlap(self.player, self.stars, self.collectStar, None, None)
        #  Reset the self.players velocity (movement)
        self.player.body.velocity.x = 0
        if self.cursors.left.isDown:
            #  Move to the left
            self.player.body.velocity.x = -150
            self.player.animations.play('left')
        elif self.cursors.right.isDown:
            #  Move to the right
            self.player.body.velocity.x = 150
            self.player.animations.play('right')
        else:
            #  Stand still
            self.player.animations.stop()
            self.player.frame = 4
        #  Allow the self.player to jump if they are touching the ground.
        if self.cursors.up.isDown and self.player.body.touching.down:
            self.player.body.velocity.y = -350


GAME = Game()
window.GAME = GAME
