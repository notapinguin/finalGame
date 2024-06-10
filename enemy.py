from ursina import *
import config
import time

class Enemy(Entity):
    def __init__(self, player=None, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None, health=100, tag='enemy'):
        super().__init__(model='cube', scale=scale, position=position, texture=texture, collider='box', tag=tag)
        self.health = health
        self.collider = BoxCollider(entity=self)  # Set collider size to match scale
        self.alive = True
        self.player = player
        self.dash_speed = 90  # Adjust this value as needed for the dash speed
        self.speed = 5
        self.dash_cooldown = 1  # Dash cooldown timer
        self.dash_timer = 0  # Timer to keep track of dash cooldown
        self.type = 'melee'

        self.framesBackLeft = [
            'assets/meleeEnemy/enemyBackLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackLeft/frame_5_delay-0.2s'
        ]
        
        self.framesBackRight = [
            'assets/meleeEnemy/enemyBackRight/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyBackRight/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyBackRight/frame_5_delay-0.2s'
        ]
        
        self.framesForwardsRight = [
            'assets/meleeEnemy/enemyForwardsRight/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsRight/frame_5_delay-0.2s'
        ]
        
        self.framesForwardsLeft = [
            'assets/meleeEnemy/enemyForwardsLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemy/enemyForwardsLeft/frame_5_delay-0.2s'
        ]

        self.frameCount = 0
        self.frameDelay = 0.1
        self.lastFrame = 0

    def take_damage(self):
        self.health -= 50
        if self.health <= 0:
            invoke(destroy, self)
            self.alive = False
            print("Killed an enemy")
            config.kills += 1

    def attackPlayer(self):
        player_position = self.player.position
        direction = (player_position - self.position).normalized()
        distance = distance_2d(self, self.player)
        
        # Update dash cooldown timer
        self.dash_timer = max(0, self.dash_timer - time.dt)
        
        # If not dashing, move towards the player at normal speed
        if distance > 5:
            self.position += direction * 10 * time.dt  # Move faster towards the player
        elif distance > 0.75:
            self.position += direction * self.speed * time.dt
        elif distance <= 0.75 and self.dash_timer <= 0:  # Check if dash is off cooldown
            self.animate_position(self.position + Vec3(direction.x, direction.y, 0) * 2, duration=0.2, curve=curve.linear)
            self.dash_timer = self.dash_cooldown  # Start the dash cooldown timer

    def updateAnimation(self):
        relativePosition = self.position - self.player.position
        if relativePosition.x >= 0 and relativePosition.y >= 0:
            print("Top Right")
            self.update_animation(self.framesBackLeft)
        elif relativePosition.x < 0 and relativePosition.y > 0:
            print("Top Left")
            self.update_animation(self.framesBackRight)
        elif relativePosition.x <= 0 and relativePosition.y <= 0:
            print("Bottom Left")
            self.update_animation(self.framesForwardsRight)
        elif relativePosition.x > 0 and relativePosition.y < 0:
            print("Bottom Right")
            self.update_animation(self.framesForwardsLeft)

    def update_animation(self, frames):
        self.frames = frames
        self.lastFrame += time.dt
        if self.lastFrame >= self.frameDelay:
            self.frameCount += 1
            if self.frameCount > 5:
                self.frameCount = 0
            self.texture = self.frames[self.frameCount]
            self.lastFrame = 0
