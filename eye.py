from ursina import *  # import the ursina game engine
from player import Player  # import the player class
from random import uniform  # import the uniform function from the random module
import config  # import the configuration module

class eye(Entity):
    # eye class inherits from ursina's entity class
    def __init__(self, player=None, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None, health=100, tag='enemy'):
        super().__init__(model='cube', scale=scale, position=position, texture=texture, collider='box', tag='enemy')
        # initialize the eye entity with a cube model, box collider, specified position, scale, texture, and tag 'enemy'
        self.health = health  # set the health of the eye
        self.collider = BoxCollider(entity=self)  # set collider size to match scale
        self.alive = True  # set the alive status to true
        self.player = player  # assign the player instance
        self.speed = 5  # set the movement speed
        self.atkRange = 2  # set the attack range
        self.inAtkRange = 0  # initialize in attack range timer
        self.currentDirection = Vec3(0, 0, 0)  # initialize current direction vector
        self.bullet = None  # initialize bullet to none
        self.type = 'ranged'  # set enemy type to ranged
        self.tag = 'enemy'  # set tag to 'enemy'
        self.frameCount = 0  # initialize frame count
        self.frameDelay = 0.1  # set delay between frames
        self.lastFrame = 0  # initialize last frame time
        self.framesBackLeft = [  # list of frame textures for back left animation
            'assets/meleeEnemy/enemyBackLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_5_delay-0.2s'
        ]
        
        self.framesBackRight = [  # list of frame textures for back right animation
            'assets/meleeEnemy/enemyBackRight/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackRight/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_5_delay-0.2s'
        ]
        
        self.framesForwardsLeft = [  # list of frame textures for forwards left animation
            'assets/eyeEnemy/eyeForwardsLeft/frame_0_delay-0.2s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_1_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_2_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_3_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_4_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_5_delay-0.2s'
        ]

        self.framesForwardsRight = [  # list of frame textures for forwards right animation
            'assets/eyeEnemy/eyeForwardsRight/frame_0_delay-0.2s',
            'assets/eyeEnemy/eyeForwardsRight/frame_1_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_2_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_3_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_4_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_5_delay-0.2s'
        ]
        
        self.framesBackLeftRed = [  # list of frame textures for red back left animation
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_5_delay-0.2s'
        ]

        self.framesBackRightRed = [  # list of frame textures for red back right animation
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_0_delay-0.2s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_1_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_2_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_3_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_4_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_5_delay-0.2s'
        ]

        self.framesForwardsLeftRed = [  # list of frame textures for red forwards left animation
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_0_delay-0.2s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_1_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_2_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_3_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_4_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_5_delay-0.2s'
        ]

        self.framesForwardsRightRed = [  # list of frame textures for red forwards right animation
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_0_delay-0.2s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_1_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_2_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_3_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_4_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_5_delay-0.2s'
        ]
        
    def take_damage(self):
        # handle taking damage
        self.health -= 50  # reduce health by 50
        if self.health <= 0:
            self.alive = False  # set alive status to false if health is 0 or less
            invoke(destroy, self)  # destroy the entity
            print("killed an enemy")  # print message indicating an enemy was killed (for debugging)
            config.kills += 1  # increment kill count in config

    def attackPlayer(self):
        # handle attacking the player
        playerDirection = (self.player.position - self.position).normalized()  # calculate direction to player
        distanceToPlayer = distance_2d(self, self.player)  # calculate distance to player

        if distanceToPlayer > self.atkRange:
            # if the player is outside attack range, move towards the player
            if distanceToPlayer > 5:
                self.position += playerDirection * 20 * time.dt  # move faster if out of player's vision (so that there are almost always enemies on screen)
            else:
                self.position += playerDirection * self.speed * time.dt  # move at normal speed if on screen
        elif distanceToPlayer < self.atkRange - 0.1:
            # if the player is within attack range or slightly inside, move away from the player
            self.position -= playerDirection * self.speed * time.dt  # move away from the player

        if distanceToPlayer <= self.atkRange + 2:
            # if within attack range + 2 units
            self.inAtkRange += time.dt  # increment in attack range timer
            aim = raycast(self.position, playerDirection, distance=10, debug=True)  # perform a raycast towards player (to show that they are about begin to shoot)

            if self.inAtkRange >= uniform(0.4, 0.8):
                self.color = color.red  # change color to red after a random time between 0.4 and 1.2 seconds (visual attack indicator)
            if self.inAtkRange >= 1: #shoot player
                self.color = color.white  # change color to normal after 1 second
                self.currentDirection = (self.player.position - self.position).normalized()  # recalculate direction to player
                
                self.bullet = Entity(model='sphere', color=color.red, scale=0.2, position=self.position, collider='sphere')
                # create a bullet entity
                self.bullet.animate_position(self.position + [12 * p for p in self.currentDirection], duration=1, curve=curve.linear)
                # animate the bullet's movement
                invoke(destroy, self.bullet, 1)  # destroy the bullet after 1 second
                self.inAtkRange = 0  # reset in attack range timer
        else:
            self.color = color.white  # reset color to white if out of attack range
            self.inAtkRange = 0  # reset in attack range timer

    def updateAnimation(self):
        # update the animation based on relative position to player
        relativePosition = self.position - self.player.position  # calculate relative position to player
        if relativePosition.x >= 0 and relativePosition.y >= 0:
            self.update_animation(self.framesBackLeft)  # update animation to back left frames
        elif relativePosition.x < 0 and relativePosition.y > 0:
            self.update_animation(self.framesBackRight)  # update animation to back right frames
        elif relativePosition.x <= 0 and relativePosition.y <= 0:
            self.update_animation(self.framesForwardsRight)  # update animation to forwards right frames
        elif relativePosition.x > 0 and relativePosition.y < 0:
            self.update_animation(self.framesForwardsLeft)  # update animation to forwards left frames

    def update_animation(self, frames):
        # update the animation frames
        self.frames = frames  # frames is current set of frames
        self.lastFrame += time.dt  # increment the time since the last frame update
        if self.lastFrame >= self.frameDelay:
            self.frameCount += 1  # move to the next frame
            if self.frameCount > 5:
                self.frameCount = 0  # loop back to the first frame if at the end
            self.texture = self.frames[self.frameCount]  # update the texture to the current frame
            self.lastFrame = 0  # reset the frame timer
