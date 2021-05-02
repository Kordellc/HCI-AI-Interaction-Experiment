import pygame
from pygame.locals import *
import sys
import random
import time
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 800
WIDTH = 1200
ACC = .5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

running = True

class Player(pygame.sprite.Sprite):
    # the agent. will collect game info, parse and pass to AIAgent
    def __init__(self):
        super().__init__()
        self.xdirection = 0
        self.ydirection = 0
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(10, 120))
        self.pos = vec((10, 720))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.globalX = 10
        self.jumping = False
        self.score = 0
        self.type = "Player"

    def move(self):
        self.acc = vec(0, 0.05)

        # pressed_keys = pygame.key.get_pressed()

        if self.xdirection != 0:
            self.acc.x = -ACC* self.xdirection
            self.xdirection = 0
        # else:
        #     self.acc.x = 0
        #     self.vel.x = 0
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
            self.vel.y = -7

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self, platforms, action=[False, False, False]):
        hits = pygame.sprite.spritecollide(self, platforms, False)
    # if self.vel.y > 0:
        if hits:
            for plat in hits:
                if plat.type == "Goal":
                    if plat.point == True:  ##
                        plat.point = False  ##
                        self.score += 25  ##
                if plat.type == "Danger":
                    return True
                if self.pos.y < plat.rect.bottom and (self.pos.x - 15 < plat.rect.right and self.pos.x + 15 > plat.rect.left):
                    # if hits[0].point == True:  ##
                    #     hits[0].point = False  ##
                    #     self.score += 1  ##
                    if self.vel.y > 0:
                        self.pos.y = plat.rect.top + 1
                        self.vel.y = 0
                        self.jumping = False
                elif  self.pos.y > plat.rect.centery and (self.pos.x - 15 < plat.rect.right and self.pos.x + 15 > plat.rect.left):
                    # if hits[0].point == True:  ##
                    #     hits[0].point = False  ##
                    #     self.score += 1  ##
                    if self.vel.y < 0:
                        self.pos.y = plat.rect.bottom +30
                        self.vel.y = 0
                        self.cancel_jump()
                elif self.pos.x < plat.rect.left:
                    # if hits[0].point == True:  ##
                    #     hits[0].point = False  ##
                    #     self.score += 1  ##
                    # self.pos.x = plat.rect.left - 15
                    self.vel.x = 0
                elif self.pos.x > plat.rect.right:
                    # if hits[0].point == True:  ##
                    #     hits[0].point = False  ##
                    #     if hits[0].val == True:
                    #         self.score += 1  ##
                    #     else:
                    #         self.cost -= 1
                    # self.pos.x = plat.rect.right + 15
                    self.vel.x = 0
        if action[1] and action[0]:
            self.xdirection = 0
        elif action[0]:
            self.xdirection = 1
        elif action[1]:
            self.xdirection = -1

        if action[2]:
            self.jump(platforms)
        else :
            self.cancel_jump()


        # self.globalX += pow(self.acc.x, 3)
        if self.pos.x < 15:
            self.pos.x = 15
            self.vel.x = 0
        return False


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 30))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.type = "Platform"
        self.moving = True
        self.point = False

    def move(self):
        pass

class obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((60, 100))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.type = "Danger"
        self.moving = True
        self.point = True

    def move(self):
        pass

class goalPost(pygame.sprite.Sprite):
    def __init__(self, truth=False):
        super().__init__()
        self.surf = pygame.Surface((65, 30))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.moving = True
        self.point = True
        self.type = "Goal"
        self.check = truth

    def move(self):
        pass

    def testEnd(self):
        if self.check and not self.point:
            return True
        return False


class Game():
    def __init__(self, show=True, human=True):
        # GET LEVEL
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.things = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.P1 = Player()
        self.laser = obstacle()
        self.score = 0
        self.displaysurface = None
        self.running = True
        self.show = show
        self.reset(show)
        self.coop = human




    def reset(self, show=True, human=True):
        # global go
        pygame.init()
        if show:
            pygame.init()
            self.displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("HCI-Experiment")
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.things = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.P1 = Player()
        self.laser = obstacle()
        self.score = 0
        self.running = True
        self.coop = human
        self.show = show
        self.all_sprites.add(self.P1)
        self.laser.surf = self.laser.surf.get_rect(center=(2, 760))
        self.laser.surf = pygame.Surface((4, HEIGHT))
        self.laser.surf.fill((255, 0, 0))
        self.laser.rect = self.laser.surf.get_rect(center=(0, HEIGHT / 2))
        self.platforms.add(self.laser)
        self.obstacles.add(self.laser)
        self.all_sprites.add(self.laser)

        self.P1.pos = vec((WIDTH / 2, HEIGHT - 80))
        self.P1.vel = vec(0, 0)
        self.P1.acc = vec(0, 0)
        PT1 = platform()
        PT1.surf = pygame.Surface((WIDTH, 40))
        PT1.surf.fill((0, 0, 255))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 20))
        self.all_sprites.add(PT1)
        self.platforms.add(PT1)

        # C1 = goalPost()
        # C1.rect = C1.surf.get_rect(center=(WIDTH / 4, 180))
        # self.platforms.add(C1)
        # self.things.add(C1)
        # self.coins.add(C1)
        # self.all_sprites.add(C1)
        #
        # C2 = goalPost()
        # C2.rect = C2.surf.get_rect(center=(WIDTH / 4 + WIDTH /2 , 180))
        # self.platforms.add(C2)
        # self.coins.add(C2)
        # self.things.add(C2)
        # self.all_sprites.add(C2)


        self.obj_gen()

        self.score = 0
        self.P1.score = 0
        self.running = True
        PT1.point = False

    def update(self, action=[False, False, False]):
        override = False
        if self.show:
            self.displaysurface.fill((0, 0, 0))
            f = pygame.font.SysFont("Verdana", 20)
            # a = f.render(str(self.score), True, (0, 255, 0))
            b = f.render(str(self.getScore()), True, (123, 255, 0))
            # c = f.render(str(self.P1.cost), True, (123, 255, 123))
            # displaysurface.blit(a, (WIDTH / 2 - WIDTH / 4, 10))
            self.displaysurface.blit(b, (WIDTH / 2, 10))
            # displaysurface.blit(c, (WIDTH / 2 + WIDTH / 4, 10))
        for entity in self.all_sprites:
            if self.show:
                self.displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        if self.P1.rect.top > HEIGHT:
        #     self.P1.pos.x = 5
            self.P1.pos.y = HEIGHT - 100
        #     self.P1.score = self.P1.score - 10
        push = (self.score / 5000 + 1)
        if self.P1.pos.x >= WIDTH / 2:  # side-scroller
            if self.laser.rect.x > 0:
                if self.laser.rect.x > push:
                    self.laser.rect.x -= push*1.5-1
                else:
                    self.laser.rect.x = 0
            self.P1.pos.x -= abs(self.P1.vel.x)+2.5
            # self.P1.vel.x = 0;
            self.score += round((abs(self.P1.vel.x)+1) / 10)
            for plat in self.things:
                plat.rect.x -= abs(self.P1.vel.x) * push/2.5
                # plat.rect.x -= abs(self.P1.pos.x - self.posx)
                # plat.rect.x -= abs(self.P1.vel.x/2)
                if plat.rect.right < 0:
                    plat.kill()
        else:
            self.laser.rect.x += push
        x = action
        self.obj_gen()
        if self.show:
            pygame.display.update()
            # FramePerSec.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    # self.endGame()
                    global running
                    running = False
                    self.running = False
                    pygame.quit()
                    return False, self.getScore(), override
        # self.P1.update(self.platforms)
        # keys = pygame.key.get_pressed()
            if self.coop:
                pressed = pygame.key.get_pressed()

                up, left, right, freeze = [pressed[key] for key in (K_w, K_a, K_d, K_s)]
                override = False
                if up or left or right or freeze:
                    override = True
                    x = [False, False, False]
                if left:
                    x[0] = True
                if right:
                    x[1] = True
                if up:
                    x[2] = True
        if(self.P1.update(self.platforms, x)):
            self.endGame()

        return self.running, self.getScore(), override
    # def load(self):

    def endGame(self):
        self.running = False
        if self.show:
            pygame.quit()
    def getScore(self):
        return round(self.score + self.P1.score)


    def getEnviroment(self):
        visible = []
        visible.append(self.score)
        visible.append(self.laser.rect.x)
        visible.append(self.P1.pos.x)
        visible.append(self.P1.pos.y)
        for coin in self.coins:
            visible.append(coin.rect.x)
            visible.append(coin.rect.y)
            visible.append(coin.point)

        for block in self.obstacles:
            visible.append(block.rect.x)
            visible.append(block.rect.y)

        return visible


    def check(self, platform, groupies):
        if pygame.sprite.spritecollideany(platform,groupies):
            return True
        else:
            for entity in groupies:
                if entity == platform:
                    continue
                if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                    return True
            C = False

    def obj_gen(self):
        while len(self.coins) < 3:
            width = random.randrange(50, 100)
            o = goalPost()
            C = True
            while C:
                o = goalPost()
                o.rect.center = (random.randrange(WIDTH - width, WIDTH*2), random.randrange(HEIGHT - 350, HEIGHT - 100))
                C = self.check(o, self.things)
            self.things.add(o)
            self.coins.add(o)
            self.platforms.add(o)
            self.all_sprites.add(o)
        while len(self.obstacles) < 3:
            width = random.randrange(50, 100)
            C = True
            while C:
                o = obstacle()
                o.rect.center = (random.randrange((WIDTH - width), (WIDTH * 2 - width)),
                                 random.randrange(HEIGHT - 300, HEIGHT - 60))
                C = self.check(o, self.things)
            self.things.add(o)
            self.obstacles.add(o)
            self.platforms.add(o)
            self.all_sprites.add(o)


# #
# #
# g = Game()
# x = True
# while True:
#     g.reset()
#     x = True
#     while x:
#         x, __, __ = g.update()
#         a = g.getEnviroment()
# # pygame.quit()
# # # #         # sys.exit()aaaa
