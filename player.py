from ursina import *  # import the ursina game engine
import config  # import the config module

class Player(Entity):
    # player class inherits from ursina's entity class
    def __init__(self, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None):
        super().__init__(model='cube', collider='box', scale=scale, position=position, texture=texture, tag='player')
        # initialize the player with a cube model, box collider, specified position, scale, texture, and a tag 'player'
        
        self.frames = ['assets/c1.gif', 'assets/c2.gif', 'assets/c3.gif']  # list of frame textures for animation
        self.collider.scale = (0.25, 0.25, 0.25)  # adjust the collider scale
        self.frameCount = 0  # current frame index
        self.frameDelay = 0.1  # delay between frame updates
        self.lastFrame = 0  # time since the last frame update
        self.dashSpeed = 50  # speed of dashing
        self.dashCooldown = 0.75  # cooldown time between dashes
        self.health = 100  # player's health
        self.alive = True  # player's alive status
        self.iFrameTime = 0.5  # invincibility frame duration after dashing
        self.iTime = 0  # current invincibility time
        self.damageCooldown = 0.2  # cooldown time for taking damage
        self.lastDamageTime = 0  # time of last damage taken

    def update_animation(self):
        # update the player's animation based on movement
        if (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']):
            self.lastFrame += time.dt  # increment the time since the last frame update
            if self.lastFrame >= self.frameDelay:
                self.frameCount += 1  # move to the next frame
                if self.frameCount > 2:
                    self.frameCount = 0  # loop back to the first frame if at the end
                self.texture = self.frames[self.frameCount]  # update the player's texture to the current frame
                self.lastFrame = 0  # reset the frame timer
        else:
            self.texture = self.frames[0]  # set the texture to the first frame when not moving

    def move(self):
        # handle player movement
        self.y += (held_keys['w'] - held_keys['s']) * 4 * time.dt  # move up/down
        self.x += (held_keys['d'] - held_keys['a']) * 4 * time.dt  # move left/right

    def dash(self):
        # handle player dashing
        if self.dashCooldown <= 0 and held_keys['shift'] and self.iTime <= 0:
            direction = Vec3(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s'], 0).normalized()
            # calculate the dash direction based on input
            self.position += direction * self.dashSpeed * time.dt  # update the position based on dash speed and direction
            self.dashCooldown = 0.5  # reset the dash cooldown
            self.iTime = 0.2  # set invincibility time
            self.collider = None  # disable collider during dash
        
        self.dashCooldown = max(0, self.dashCooldown - time.dt)  # reduce dash cooldown over time
        self.iTime = max(0, self.iTime - time.dt)  # reduce invincibility time over time
        if self.iTime <= 0:
            self.collider = 'box'  # re-enable collider after invincibility time

    def playerAttack(self):
        # handle player attacking
        x, y, z = mouse.position  # get mouse position
        realPos = self.position + (camera.fov * x, camera.fov * y, 0)  # calculate the attack position relative to player
        direction = Vec3(realPos[0] - self.x, realPos[1] - self.y, 0).normalized()  # calculate attack direction
        bullet = Entity(model='sphere', color=color.blue, scale=0.08, position=self.position, collider='sphere', tag='attack')
        # create a bullet entity
        bullet.animate_position(self.position + [24 * p for p in direction], duration=0.5, curve=curve.linear)
        # animate the bullet's movement
        shoot = raycast(self.position, direction, distance=10, ignore=[self, bullet])
        # perform a raycast to detect collisions
        if shoot.hit and shoot.entity.tag == 'enemy' and shoot.hit is not None:
            shoot.entity.take_damage()  # apply damage to the enemy if hit
            print("damaged an enemy!")
        
        invoke(destroy, bullet, delay=0.5)  # destroy the bullet after a delay

    def damage(self):
        # handle player taking damage
        if time.time() - self.lastDamageTime >= self.damageCooldown:
            # check if enough time has passed since the last damage
            self.health -= 15  # reduce player's health
            self.lastDamageTime = time.time()  # update the time of last damage taken
            self.texture = 'assets/c1damage'  # change texture to indicate damage
