from ursina import *  # import the ursina game engine
import config  # import the config module
import time  # import the time module

class Enemy(Entity):  # define the enemy class, which inherits from entity
    def __init__(self, player=None, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None, health=100, tag='enemy'):
        super().__init__(model='cube', scale=scale, position=position, texture=texture, collider='box', tag=tag)  # initialize the entity with a cube model, given scale, position, texture, and collider
        self.health = health  # set the health of the enemy
        self.collider = BoxCollider(entity=self)  # set collider size to match scale
        self.alive = True  # set the enemy's alive status to true
        self.player = player  # set the player object
        self.dash_speed = 90  # set the dash speed
        self.speed = 5  # set the movement speed
        self.dash_cooldown = 1  # set the dash cooldown timer
        self.dash_timer = 0  # initialize the dash timer
        self.type = 'melee'  # set the enemy type to melee

        self.framesBackLeft = [  # list of frames for moving back left
            'assets/meleeEnemy/enemyBackLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_5_delay-0.2s'
        ]
        
        self.framesBackRight = [  # list of frames for moving back right
            'assets/meleeEnemy/enemyBackRight/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackRight/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_5_delay-0.2s'
        ]
        
        self.framesForwardsRight = [  # list of frames for moving forwards right
            'assets/meleeEnemy/enemyForwardsRight/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_5_delay-0.2s'
        ]
        
        self.framesForwardsLeft = [  # list of frames for moving forwards left
            'assets/meleeEnemy/enemyForwardsLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_5_delay-0.2s'
        ]

        self.frameCount = 0  # initialize the frame counter
        self.frameDelay = 0.1  # set the delay between frames
        self.lastFrame = 0  # initialize the last frame time

    def take_damage(self):  #called every time player damages enemy 
        self.health -= 50  # reduce the health 
        if self.health <= 0:  # check if health is less than or equal to 0
            invoke(destroy, self)  # destroy the enemy
            self.alive = False  # set alive status to false
            print("Killed an enemy")  # print message for debugging purposes 
            config.kills += 1  # increment the kill count in

    def attackPlayer(self):  # attacking player
        player_position = self.player.position  # get the player's position
        direction = (player_position - self.position).normalized()  # calculate the direction to the player
        distance = distance_2d(self, self.player)  # calculate the 2d distance to the player
        
        # update dash cooldown timer
        self.dash_timer = max(0, self.dash_timer - time.dt)  # decrement the dash timer but not below 0
        
        # if not dashing, move towards the player at normal speed
        if distance > 5:  # if enemy is out of players vision
            self.position += direction * 10 * time.dt  # move faster towards the player
        elif distance > 0.75:  # check if the distance is greater than 0.75 and less than 5
            self.position += direction * self.speed * time.dt  # move towards the player at normal speed
        elif distance <= 0.75 and self.dash_timer <= 0:  # check if distance is less than or equal to 0.75 and less than 5 and dash is off cooldown 
            self.animate_position(self.position + Vec3(direction.x, direction.y, 0) * 2, duration=0.2, curve=curve.linear)  # dash towards the player
            self.dash_timer = self.dash_cooldown  # start the dash cooldown timer

    def updateAnimation(self):  # define the updateAnimation method
        relativePosition = self.position - self.player.position  # calculate the relative position to the player
        if relativePosition.x >= 0 and relativePosition.y >= 0:  # check if in top right quadrant
            print("Top Right")  # print a message (for debugging)
            self.update_animation(self.framesBackLeft)  # update the animation to back left frames
        elif relativePosition.x < 0 and relativePosition.y > 0:  # check if in top left quadrant
            print("Top Left")  # print a message(for debugging)
            self.update_animation(self.framesBackRight)  # update the animation to back right frames
        elif relativePosition.x <= 0 and relativePosition.y <= 0:  # check if in bottom left quadrant
            print("Bottom Left")  # print a message(for debugging)
            self.update_animation(self.framesForwardsRight)  # update the animation to forwards right frames
        elif relativePosition.x > 0 and relativePosition.y < 0:  # check if in bottom right quadrant
            print("Bottom Right")  # print a message(for debugging)
            self.update_animation(self.framesForwardsLeft)  # update the animation to forwards left frames

    def update_animation(self, frames):  # define the update_animation method
        self.frames = frames  # set the frames
        self.lastFrame += time.dt  # increment the last frame time
        if self.lastFrame >= self.frameDelay:  # check if it's time to update the frame
            self.frameCount += 1  # increment the frame count
            if self.frameCount > 5:  # check if frame count exceeds the number of frames
                self.frameCount = 0  # reset the frame count
            self.texture = self.frames[self.frameCount]  # set the texture to the current frame
            self.lastFrame = 0  # reset the last frame time
