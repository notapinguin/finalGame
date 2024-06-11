from ursina import *
from player import Player
from enemy import Enemy
from random import *
from eye import eye
import config
'''
NESTED FOR LOOPS:
def count_current_enemies():
    global enemies
    current_enemies = 1
    for sublist in enemies:
        for enemy in sublist:
            if enemy.alive:
                current_enemies += 1

def spawn_enemy():
    for i in range(2):
        temp = randint(0, 100)
        if temp < 50:
            enemies[0].append(Enemy(player=player, position=(randint(-50, 50), randint(-50, 50), 0)))
        else:
            enemies[1].append(eye(player=player, position=(randint(-50, 50), randint(-50, 50), 0)))

def update()
    for i in range(2):
        spawn_enemy()
spawn enemy is a method with loop and is called in another loop, so it is a nested loop 


IF STATEMENTS:
(from player class)
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

if self.dashCooldown <= 0 and held_keys['shift'] and self.iTime <= 0:
    direction = Vec3(held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s'], 0).normalized()
    self.position += direction * self.dashSpeed * time.dt
    self.dashCooldown = 0.5
    self.iTime = 0.2
    self.collider = None

if shoot.hit and shoot.entity.tag == 'enemy' and shoot.hit != None:
    shoot.entity.take_damage()
    print("damaged an enemy!")

if time.time() - self.lastDamageTime >= self.damageCooldown:
    self.health -= 15
    self.lastDamageTime = time.time()
    self.texture = 'assets/c1damage'

    
(from enemy class)
if self.health <= 0:
    invoke(destroy, self)
    self.alive = False
    print("killed an enemy")
    config.kills += 1

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
    self.animate_position(self.position + [2* p for p in direction], duration=0.2, curve=curve.linear)
    self.dash_timer = self.dash_cooldown  # Start the dash cooldown timer


CHANGING LIST:
# Initialize lists to store different types of enemies
enemies = [[], []]
def spawn_enemy():
    for i in range(2):
        temp = randint(0, 100)
        if temp < 50:
            enemies[0].append(Enemy(player=player, position=(randint(-50, 50), randint(-50, 50), 0)))
        else:
            enemies[1].append(eye(player=player, position=(randint(-50, 50), randint(-50, 50), 0))))

def update():
        if(player.health<=0):
            player.alive = False
            player.position = (0, 0, 0)
            config.kills = 0
            
            player.health = 100
        # print("player is dead!")
            death_text = Text(text="You Died", color=color.red, position=(-0.2, 0.1), scale=5)

            invoke(destroy, death_text, 1)
            for sublist in enemies:
                for enemy in sublist:
                    invoke(destroy, enemy)
            enemies = [[], []]



            
EXTRA FEATURES:
- enemy (both types) decision tree (changes depending on player distance)
- object oriented programming used via classes:
    - all player logic is simplified and contained to player class, makes main file more readable
    - player, eye, and enemy inherit from ursina's entity class 
    - data relating to classes are stored in their respective class (eg. health values stored in player)
- visual feedback (player flashes red when damaged) and animations
- enemies spawn in random locations 
- player can dash with i frames
- health tracking and visualization with health bar
- enemy type is randomized 
- attacks can only affect player every .2 seconds to reduce difficulty 
- global cross module variable (updated in eye, enemy, and main modules) stored in a config file 
- ui elements, and a visualized health bar
- differentation between hitscan and projectile bullets:
    - player uses hitscan bullets, as their projectile speed is incredibly fast, the bullet travel time is neglegible
    - the preformance tradeoff for using projectile bullets was not worth it for the player, so hitscan bullets were used
    - enemy uses projectile bullets, as their projectile speed is slow, allowing the player to use their dash to dodge through the bullets
-  cooldowns for player to prevent people from accidentally winning (dash and attack cooldown to prevent players from spamming dash or attack)
- visual indicator for when a ranged enemy is about to attack, but randomized between 0.4 and 1.2 seconds, to enhance player skill expression and to prevent the player from memorizing dash timing to dodge bullets 
- art and animations made by us 
- high score system, and scoring system that encourages players to actually kill enemies 


Code was written by Yile
Documentation and art was done by Luke 
'''

from ursina import *
from random import randint

app = Ursina()

# set the application window to fullscreen mode
window.fullscreen = True

# enable the frames per second (fps) counter
window.fps_counter.enabled = True

# disable the entity counter
window.entity_counter.enabled = False

# disable the collider counter
window.collider_counter.enabled = False

# set the camera to orthographic mode
camera.orthographic = True

# set the field of view (fov) of the camera to 10
camera.fov = 10

# create a player object at position (0, 0, 0)
player = Player(position=(0, 0, 0))

# initialize the high score to 0
highScore = 0

# set the player as the parent for the camera
camera.parent = player

# display the high score text on the screen
highscoreText = Text(text="high score: " + str(highScore), color=color.red, position=(-0.82, 0.35), scale=1)

# set the initial attack cooldown to 0.5 seconds
attackCD = 0.5

# set the initial enemy spawn timer to 0
enemy_spawn_timer = 0

# set the min number of enemies allowed at a time to 4
MIN_ENEMIES = 4

# create a background for the health bar
health_bar_background = Entity(parent=camera.ui, model='quad', color=color.gray, scale=(0.22, 0.03), position=(-0.71, 0.45))

# create the health bar
health_bar = Entity(parent=camera.ui, model='quad', color=color.red, scale=(0.21, 0.02), position=(-0.71, 0.45))

# function to update the health bar based on the player's health
def update_health_bar():
    # update the width of the health bar based on the player's health
    health_bar.scale_x = player.health / 100 * 0.21

    # adjust the position of the health bar to align with the background
    health_bar.x = health_bar_background.x - (0.21 - health_bar.scale_x) / 2

# initialize lists to store different types of enemies
enemies = [[], []]

# display the score text on the screen
kills_text = Text(text="score: " + str(config.kills), color=color.red, position=(-0.82, 0.4), scale=1)

# function to spawn enemies
def spawn_enemy():
    for i in range(2):
        # generate a random number between 0 and 100
        temp = randint(0, 100)

        # if the random number is less than 50, spawn an enemy of type Enemy
        if temp < 50:
            enemies[0].append(Enemy(player=player, position=(randint(-50, 50), randint(-50, 50), 0)))

        # if the random number is 50 or greater, spawn an enemy of type eye
        else:
            enemies[1].append(eye(player=player, position=(randint(-50, 50), randint(-50, 50), 0)))

# function to count the current number of alive enemies
def count_current_enemies():
    # declare the global variable enemies
    global enemies

    # initialize the current number of enemies to 1
    current_enemies = 1

    # iterate over each sublist in the enemies list
    for sublist in enemies:
        # iterate over each enemy in the sublist
        for enemy in sublist:
            # if the enemy is alive, increment the current number of enemies by 1
            if enemy.alive:
                current_enemies += 1

    # return the current number of enemies
    return current_enemies

# function to spawn lights on the ground
def spawn_lights(squares):
    for i in range(squares):
        # create a light entity at a random position with a specified scale and texture
        Entity(model='quad', position=(randint(-50, 50), randint(-50, 50), 0), scale=0.5, texture='assets/LightFlower')

# main update function, called every frame
def update():
    #  global variables used in the function
    global attackCD, enemy_spawn_timer, kills_text, player, enemies, highScore, highscoreText
    
    try:
        # if the current kills are greater than the high score, update the high score
        if config.kills > highScore:
            highScore = config.kills

        # update the kills text and high score text on the screen
        kills_text.text = "kills: " + str(config.kills)
        highscoreText.text = "high score: " + str(highScore)

        # handle player death
        if player.health <= 0:
            # set the player's alive status to False and reset their position
            player.alive = False
            player.position = (0, 0, 0)

            # reset the kills count and player's health
            config.kills = 0
            player.health = 100

            # display a "you died" message on the screen
            death_text = Text(text="YOU DIED", color=color.red, position=(-0.2, 0.1), scale=5)
            invoke(destroy, death_text, 1)

            # destroy all enemies
            for sublist in enemies:
                for enemy in sublist:
                    invoke(destroy, enemy)
            enemies = [[], []]

        # update the health bar
        update_health_bar()

        # update the behavior of enemies in the first sublist
        for enemy in enemies[0]:
            if enemy.alive:
                enemy.attackPlayer()
                enemy.updateAnimation()
                if enemy.intersects(player):
                    player.damage()

        # update the behavior of enemies in the second sublist
        for enemy in enemies[1]:
            if enemy.alive:
                enemy.attackPlayer()
                enemy.updateAnimation()
                if enemy.bullet and enemy.bullet.intersects(player):
                    player.damage()

        # update the attack cooldown
        attackCD = max(0, attackCD - time.dt)
        player.update_animation()

        # handle player attacks
        if held_keys['left mouse'] and attackCD == 0:
            player.playerAttack()
            attackCD = 0.5

        # handle player movement and dash
        player.move()
        player.dash()

        # spawn new enemies if the current count is less than the min allowed
        if count_current_enemies() < MIN_ENEMIES:
            for i in range(2):
                spawn_enemy()

    except Exception as e:
        # print any exceptions that occur
        print(e)

# create a ground entity and spawn lights
spawn_lights(1000)
Entity(model='quad', texture='assets/pyrplei1', scale=600, z=1, tag='ground')

# run the application
app.run()





