import pygame
import random
import os
from os import path


WIDTH = 900
HEIGHT = 650

FPS = 60
#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# set up asserts  folders
#Windows: "C:\Moroz Python\BooktTask"
game_folder = os.path.dirname(__file__)
img_dir = os.path.join(game_folder, "image")
snd_dir = path.join(path.dirname(__file__), "snd")


#initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)






class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update (self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = +7
        if keystate[pygame.K_DOWN]:
            self.speedy = + 7
        if keystate[pygame.K_UP]:
            self.speedy = - 7
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
        if self.rect.bottom < 0:
            self.rect.bottom = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()


    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(monster_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .7 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(- 150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(- 100, -40)
            self.speedy = random.randrange(3, 9)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (60, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 10
        if self.rect.bottom < 0:
            self.kill()


    def update(self):
        self.rect.y += self.speedy

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect.center = center




# load all game graphips



background = pygame.image.load(path.join(img_dir, "background.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "myship2.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, "bullet1.png")).convert()
monster_img = []
monster_list = ['monster1.png',  'monster3.png', 'monster4.png']

for img in monster_list:
    monster_img.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player']=[]

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


#Load sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot1.wav'))
expl_sounds = pygame.mixer.Sound(path.join(snd_dir, 'kill1.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'kill1.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'background.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(12):
    newmob()

pygame.mixer.music.play(loops = -1)
score = 0

#Game loop
running = True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False


    #Update
    all_sprites.update()


    #check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        expl_sounds.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()


    #check to see if mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if player died and the explosion has finished
    if player.lives == 0 and not death_explosion.alive():
        running = False


    #Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "RSSI:"+str(score), 24, WIDTH / 2, 10)
    draw_shield(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

