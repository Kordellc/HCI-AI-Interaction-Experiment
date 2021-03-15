import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 800
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite):
    # the agent. will collect game info, parse and pass to AIAgent
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(10, 420))
        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.globalX = 10
        self.jumping = False
        self.score = 40
        self.type = "Player"

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        elif pressed_keys[K_d]:
            self.acc.x = ACC

        else:
            self.acc.x = 0
            self.vel.x = 0

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self, platforms):
        self.globalX += pow(self.acc.x, 3)
        if self.pos.x < 15:
            self.pos.x = 15
            self.vel.x = 0
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    # if hits[0].point == True:  ##
                    #     hits[0].point = False  ##
                    #     self.score += 1  ##
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                for plat in hits:
                    if plat.type == "Goal":
                        if hits[0].point == True:  ##
                            hits[0].point = False  ##
                            self.score += 100  ##
                    if self.pos.x < plat.rect.left:
                        # if hits[0].point == True:  ##
                        #     hits[0].point = False  ##
                        #     self.score += 1  ##
                        self.pos.x = plat.rect.left - 15
                        self.vel.x = 0
                    if self.pos.x > plat.rect.right:
                        # if hits[0].point == True:  ##
                        #     hits[0].point = False  ##
                        #     self.score += 1  ##
                        self.pos.x = plat.rect.right + 15
                        self.vel.x = 0


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.type = "Platform"
        self.moving = True
        self.point = True

    def move(self):
        pass

class goalPost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.moving = True
        self.point = True
        self.type = "Goal"

    def move(self):
        pass

class Game():
    def __init__(self, type, bot=None):
        # GET LEVEL
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.P1 = Player()
        self.all_sprites.add(self.P1)

        PT1 = platform()
        PT1.surf = pygame.Surface((WIDTH, 20))
        PT1.surf.fill((255, 0, 0))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

        PT2 = platform()
        PT2.surf = pygame.Surface((60, 40))
        PT2.surf.fill((255, 0, 0))
        PT2.rect = PT2.surf.get_rect(center=(WIDTH / 2, HEIGHT - 30))

        # PT3 = goalPost()
        # PT3.surf = pygame.Surface((60, 40))
        # PT3.surf.fill((0, 0, 255))
        # PT3.rect = PT3.surf.get_rect(center=(WIDTH+30, HEIGHT - 30))

        self.all_sprites.add(PT1)
        self.all_sprites.add(PT2)
        # self.all_sprites.add(PT3)
        # self.all_sprites.add(PT4)

        self.platforms = pygame.sprite.Group()
        self.platforms.add(PT1)
        self.platforms.add(PT2)
        # self.platforms.add(PT3)
        # self.platforms.add(PT4)

        PT1.point = False



    def update(self):
        self.P1.update(self.platforms)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.P1.jump(self.platforms)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.P1.cancel_jump()

        if self.P1.rect.top > HEIGHT:
                self.P1.pos.x = 5
                self.P1.pos.y = HEIGHT - 50
                self.P1.score = self.P1.score - 10
        #     #     displaysurface.fill((255, 0, 0))
        #     #     pygame.display.update()
        #     #     time.sleep(1)
        #     #     pygame.quit()
        #
        #
        #
        #
        if self.P1.pos.x >= WIDTH / 1.5:  # side-scroller
            self.P1.pos.x -= abs(self.P1.vel.x)
            # for plat in self.obstacles:
        #         #plat.rect.x -= abs(self.P1.pos.x - self.posx)
        #         plat.rect.x -= abs(self.P1.vel.x)
        #         if plat.rect.right < 0:
        #             plat.kill()
        # #
        # self.posx = self.P1.pos.x
        # plat_gen()
        displaysurface.fill((0, 0, 0))
        f = pygame.font.SysFont("Verdana", 20)
        g = f.render(str(self.P1.score), True, (123, 255, 0))
        displaysurface.blit(g, (WIDTH / 2, 10))

        for entity in self.all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)
    # def load(self):


    def getEnviroment(self):
        enviroTest = []

        for y in range(32):
            l = 0
            enviroMap = []
            for x in range(32):
                filled = False
                for sprites in self.all_sprites:
                    if (sprites.rect.right >= (x+1)* 25 and sprites.rect.left <= (x+1)* 25) and (sprites.rect.top <= (y+1)* 25 and sprites.rect.bottom>= (y+1)* 25) and not filled:
                        if sprites.type == "Platform":
                            enviroMap.append(.25)
                            filled = True
                        elif sprites.type == "Player":
                            enviroMap.append(.5)
                            filled = True
                        elif sprites.type == "Danger":
                            enviroMap.append(-1)
                            filled = True
                        elif sprites.type == "Goal":
                            enviroMap.append(1)
                            filled = True

                if not filled:
                    enviroMap.append(0)
            enviroTest.append(enviroMap)
        return enviroTest

# def check(platform, groupies):
#     if pygame.sprite.spritecollideany(platform,groupies):
#         return True
#     else:
#         for entity in groupies:
#             if entity == platform:
#                 continue
#             if (abs(platform.rect.top - entity.rect.bottom) > 40) and (abs(platform.rect.bottom - entity.rect.top) > 40):
#                 return True
#         C = False

# def plat_gen():
#     while len(platforms) < 6:
#         width = random.randrange(50, 100)
#         p = platform()
#         C = True
#
#         while C:
#             p = platform()
#             p.rect.center = (random.randrange(0, WIDTH - width),
#                              random.randrange(-50, 0))
#             C = check(p, platforms)
#         platforms.add(p)
#         all_sprites.add(p)




g = Game(1)
while True:
    g.update()
    g.getEnviroment()
