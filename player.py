from ursina import *
import config

class Player(Entity):
    #ENABLE DAMAGE
    def __init__(self, position=(0, 0, 0), scale=(0.5, 0.5, 0.5), texture=None):
        super().__init__(model='cube', collider='box', scale=scale, position=position, texture=texture, tag='player')
        self.frames = ['assets/c1.gif', 'assets/c2.gif', 'assets/c3.gif']
        self.collider.scale = (0.25, 0.25, 0.25)
        self.frameCount = 0
        self.frameDelay = 0.1
        self.lastFrame = 0
        self.dashSpeed = 50
        self.dashCooldown = 0.75
        self.health = 100
        self.alive = True
        self.iFrameTime = 0.5
        self.iTime = 0
        self.damageCooldown = 0.2  # Cooldown time for taking damage
        self.lastDamageTime = 0     # Time of last damage taken

    def update_animation(self):

            if (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']):
                self.lastFrame += time.dt
                if self.lastFrame >= self.frameDelay:
                    self.frameCount += 1
                    if self.frameCount > 2:
                        self.frameCount = 0
                    self.texture = self.frames[self.frameCount]
                    self.lastFrame = 0
            else:
                self.texture = self.frames[0]
                

    def move(self):
        self.y += (held_keys['w'] - held_keys['s']) * 4 * time.dt
        self.x += (held_keys['d'] - held_keys['a']) * 4* time.dt

    def dash(self):
        if self.dashCooldown <= 0 and held_keys['shift'] and self.iTime <= 0:
            direction = Vec3(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s'], 0).normalized()
            self.position += direction * self.dashSpeed * time.dt
            self.dashCooldown = 0.5
            self.iTime = 0.2
            self.collider = None
        
        self.dashCooldown = max(0, self.dashCooldown - time.dt)
        self.iTime = max(0, self.iTime - time.dt)
        if self.iTime <= 0:
            self.collider = 'box'

    def playerAttack(self):
        x, y, z = mouse.position
        realPos = self.position + (camera.fov * x, camera.fov * y, 0)
        direction = Vec3(realPos[0] - self.x, realPos[1] - self.y, 0).normalized()
        bullet = Entity(model='sphere', color=color.blue, scale=0.08, position=self.position, collider='sphere', tag='attack')
        bullet.animate_position(self.position + [24 * p for p in direction], duration=0.5, curve=curve.linear)
        shoot = raycast(self.position, direction, distance=10, ignore=[self, bullet])
        if shoot.hit and shoot.entity.tag == 'enemy' and shoot.hit != None:
            shoot.entity.take_damage()
            print("damaged an enemy!")
        
        invoke(destroy, bullet, delay=0.5)

    def damage(self):
        # Check if enough time has passed since the last damage
        if time.time() - self.lastDamageTime >= self.damageCooldown:
            #print("Player damaged!")
            self.health -= 15

            self.lastDamageTime = time.time()
            self.texture = 'assets/c1damage'




