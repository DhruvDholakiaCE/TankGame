from pygame import *
import math
import random

mixer.init()

mixer.Channel(0).play(mixer.Sound('tankBackgroundMusic.wav'))

fireSound = mixer.Sound('Cannon+3.wav')

explosionSound  = mixer.Sound('Bomb+2.wav')

init()

screenHeight = 700
screenWidth = 900
gameWindow = display.set_mode([screenWidth,screenHeight])
angle = 0
power = 10
gameOver = False
explosionList = []

for i in range(8):
    img = image.load('explosionAnimation/regularExplosion0'+str(i+1)+'.png').convert_alpha()
    img.set_colorkey((255,255,255))
    img = transform.scale(img,(120, 120))

    explosionList.append(img)

clock = time.Clock()
bg = image.load('tankGameBackground.jpg')



class Explosion(sprite.Sprite):
    def __init__(self, center):
        sprite.Sprite.__init__(self)

        self.image = image.load('tank.png').convert_alpha()
        self.image = explosionList[0]
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame = 0
        self.last_update = time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosionList):
                self.kill()
            else:
                center= self.rect.center
                self.image = explosionList[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class PlayerLeft(sprite.Sprite):
    def __init__(self,x,y,color):
        sprite.Sprite.__init__(self)

        self.image = image.load('tank.png').convert_alpha()

        self.image = transform.scale(self.image, (120,120))
        self.image = transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.bullet = None
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = 0
        self.life = 100

    def shootBullet(self, angle, power):
        self.bullet = Bullet(pLeft.rect.centerx,  pLeft.rect.top, angle, power)

        bulletGroup.add(self.bullet)
        all_sprites.add(self.bullet)

    def update(self):
        self.speedx =0
        keystate = key.get_pressed()
        if keystate[K_LEFT] :
            self.speedx = -5
        if keystate[K_RIGHT] :
            self.speedx= 5

        self.rect.x +=self.speedx
        # if self.rect.top < 2:
        #     self.rect.top = 2
        # if self.rect.bottom > screenHeight-2:
        #     self.rect.bottom = screenHeight-2


class Bullet(sprite.Sprite):
    def __init__(self,x,y, angle, power):
        sprite.Sprite.__init__(self)
        self.image = image.load('fireball.png').convert_alpha()
        self.startX = x
        self.startY = y
        self.image = transform.scale(self.image, (40, 40))
        self.image = transform.flip(self.image, True, True)
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0
        self.gravity = -0.2
        self.power = power
        self.angle = angle
        self.rad = math.radians(self.angle)
        self.dt = 0.1



    def update(self):

        self.speedx = math.cos(self.rad) * self.power
        self.speedy = math.sin(self.rad) * self.power
        self.distx = self.speedx * self.dt
        self.disty = self.speedy * self.dt + (self.gravity * (self.dt**2) /2)
        self.rect.x  = self.startX + self.distx
        self.rect.y = self.startY - self.disty
        self.dt += 0.5


        # if self.rect.bottom >= screenHeight - 5:
        #     self.speedy *= -1
        #     self.speedx *= -1
        # if  self.rect.x < 0 or self.rect.x > screenWidth - self.image.get_width():
        #     self.image = transform.flip(self.image, True, True)
        #     self.updateX()
        #
        # if self.rect.bottom > screenHeight or  self.rect.top < 0 :
        #     self.updateY()

img = image.load('ground.png').convert_alpha()

#............Making Left and Right Player.........................
pLeft = PlayerLeft(150, screenHeight-100, (0,255,243))

pRight = PlayerLeft(screenWidth-200, screenHeight- 100, (0,255,243))
pRight.image = transform.flip(pRight.image, True, False)

#............Adding players and bullets to sprite group...........
all_sprites = sprite.Group()
all_sprites.add(pRight)
playerGroup = sprite.Group()
playerGroup.add(pLeft, pRight)
bulletGroup = sprite.Group()
all_sprites.add(pLeft)

# defining font
fnt = font.SysFont(None, 50)

while not gameOver:
    gameWindow.fill((0, 0, 0))
    gameWindow.blit(bg, (0,0))
    for ev in event.get():
        if ev.type == QUIT :
            gameOver = True
        if ev.type == KEYDOWN:

            if ev.key == K_DOWN and angle >= 5  :
                angle -= 5
            if ev.key == K_UP :
                angle += 5
            if ev.key == K_w:
                power += 0.2
            if ev.key == K_s:
                power -= 0.2
            if ev.key == K_SPACE:
                mixer.Channel(1).play(fireSound)
                pLeft.shootBullet(angle, power)


    startx = 0


    if pLeft.bullet:    #collde only when Bullet is there
        # ......collision with ground............
        if pLeft.bullet.rect.bottom >= screenHeight - 100:
            pLeft.bullet.kill()
            pLeft.bullet = None
            angle = 0
            power = 10
        # ......Bullet Collision with Tank..........
        if pRight:
            hits = sprite.spritecollide(pRight, bulletGroup, True)

            if hits:

                mixer.Channel(2).play(explosionSound)
                exp = Explosion(pRight.rect.center)
                all_sprites.add(exp)
                pRight.kill()
                pRight = None
                angle = 0
                power = 10

    for i in range(20):

        gameWindow.blit(img, ( i*img.get_width(), screenHeight-img.get_height()-50))
    fntShow  = fnt.render('angle = ' + str(angle), True, (0,255,0) )
    powerShow = fnt.render('power = ' + str(power), True, (0,255,0))
    gameWindow.blit(fntShow, (10,10))
    gameWindow.blit(powerShow, (screenWidth - 250, 10))
    all_sprites.draw(gameWindow)

    all_sprites.update()
    display.update()
    clock.tick(100)
quit()
