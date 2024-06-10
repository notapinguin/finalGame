from ursina import *
from player import Player
from random import uniform
import config

class eye(Entity):
    def __init__(self, player=None, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None, health=100, tag='enemy'):
        super().__init__(model='cube', scale=scale, position=position, texture=texture, collider='box', tag='enemy')
        self.health = health
        self.collider = BoxCollider(entity=self)  # Set collider size to match scale
        self.alive = True
        self.player = player
        self.speed = 5
        self.atkRange = 2
        self.inAtkRange = 0
        self.currentDirection = Vec3(0, 0, 0)
        self.bullet = None
        self.type = 'ranged'
        self.tag = 'enemy'
        self.frameCount = 0
        self.frameDelay = 0.1
        self.lastFrame = 0
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
        self.framesForwardsLeft = [
            'assets/eyeEnemy/eyeForwardsLeft/frame_0_delay-0.2s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_1_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_2_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_3_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_4_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsLeft/frame_5_delay-0.2s'
        ]

        self.framesForwardsRight = [
            'assets/eyeEnemy/eyeForwardsRight/frame_0_delay-0.2s',
            'assets/eyeEnemy/eyeForwardsRight/frame_1_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_2_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_3_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_4_delay-0.1s',
            'assets/eyeEnemy/eyeForwardsRight/frame_5_delay-0.2s'
        ]
        self.framesBackLeftRed = [
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_0_delay-0.2s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_1_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_2_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_3_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_4_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackLeft/frame_5_delay-0.2s'
        ]

        self.framesBackRightRed = [
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_0_delay-0.2s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_1_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_2_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_3_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_4_delay-0.1s', 
            'assets/meleeEnemyRed/eyeEnemyRedBackRight/frame_5_delay-0.2s'
        ]

        self.framesForwardsLeftRed = [
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_0_delay-0.2s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_1_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_2_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_3_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_4_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsLeft/frame_5_delay-0.2s'
        ]

        self.framesForwardsRightRed = [
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_0_delay-0.2s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_1_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_2_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_3_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_4_delay-0.1s',
            'assets/eyeEnemyRed/eyeEnemyRedForwardsRight/frame_5_delay-0.2s'
        ]
        

    def take_damage(self):
        self.health -= 50
        if self.health <= 0:
            self.alive = False
            invoke(destroy, self)
            print("killed an enemy")
            config.kills +=1

    def attackPlayer(self):

        playerDirection = (self.player.position - self.position).normalized()
        distanceToPlayer = distance_2d(self, self.player)

        if distanceToPlayer > self.atkRange:
            # If the player is outside attack range, move towards the player
            if(distanceToPlayer > 5):
                
                self.position += playerDirection * 20 * time.dt
            else:
                
                self.position += playerDirection * self.speed * time.dt

            
        elif distanceToPlayer < self.atkRange - 0.1:  
            # If the player is within attack range, and slightly inside, move away from the player
            self.position -= playerDirection * self.speed * time.dt
        if(distanceToPlayer<=self.atkRange+2):
            self.inAtkRange += time.dt
            aim = raycast(self.position, playerDirection, distance=10, debug=True)

            if(self.inAtkRange>= uniform(0.4, 1.2)):
                self.color = color.red
            if(self.inAtkRange>=1):
                self.color = color.white
                self.currentDirection = (self.player.position - self.position).normalized()
                
                self.bullet = Entity(model='sphere', color=color.red, scale=0.2, position=self.position, collider='sphere')
                self.bullet.animate_position(self.position + [12 * p for p in self.currentDirection], duration=1, curve=curve.linear)
                
                

                invoke(destroy, self.bullet, 1)
                self.inAtkRange = 0
                
                

        else:
            self.color = color.white
            self.inAtkRange = 0





    def updateAnimation(self):
        relativePosition = self.position - self.player.position
        if relativePosition.x >= 0 and relativePosition.y >= 0:
            self.update_animation(self.framesBackLeft)
        elif relativePosition.x < 0 and relativePosition.y > 0:
            self.update_animation(self.framesBackRight)
        elif relativePosition.x <= 0 and relativePosition.y <= 0:
            self.update_animation(self.framesForwardsRight)
        elif relativePosition.x > 0 and relativePosition.y < 0:
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

   



            
            
        
