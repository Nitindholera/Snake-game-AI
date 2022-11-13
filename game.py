import random
import pygame
import numpy as np
from mlp import neural_network

class cube(object):
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx, self.pos[1]+self.dirny)

    def draw(self, surface):
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.food = None

        self.deaths = 0
        self.score = []
        self.avg_steps = []
        self.penalities = []

    def move_with_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move_with_brain(self, dis, b):
        if dis:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        inp = self.get_surroundings()
        x = b.forward_prop(inp)
        # print(x[0])
        val = x[0].argmax()

        if val == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif val == 1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif val == 2:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif val == 3:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  

    def get_surroundings(self):
        # will return an 12 size list
        re = [0,0,0,0,0,0,0,0,0,0,0,0]

        if self.head.pos[0] == 0:
            re[0] = 1
        if self.head.pos[0] == rows-1:
            re[1] = 1
        if self.head.pos[1] == 0:
            re[2] = 1
        if self.head.pos[1] == rows - 1:
            re[3] = 1
        if self.dirnx == -1:
            re[4] = 1
        if self.dirnx == 1:
            re[5] = 1
        if self.dirny == -1:
            re[6] = 1
        if self.dirny == 1:
            re[7] = 1
        if self.food.pos[0] < self.head.pos[0]:
            re[8] = 1
        if self.food.pos[0] > self.head.pos[0]:
            re[9] = 1
        if self.food.pos[1] < self.head.pos[1]:
            re[10] = 1
        if self.food.pos[1] > self.head.pos[1]:
            re[11] = 1
        for x in range(1, len(self.body)):
            if self.body[x].pos[1] == self.head.pos[1] and self.body[x].pos[0] == self.head.pos[0] - 1:
                re[0] = 1 
            if self.body[x].pos[1] == self.head.pos[1] and self.body[x].pos[0] == self.head.pos[0] + 1:
                re[1] = 1 
            if self.body[x].pos[0] == self.head.pos[0] and self.body[x].pos[1] == self.head.pos[1] - 1:
                re[2] = 1 
            if self.body[x].pos[0] == self.head.pos[0] and self.body[x].pos[1] == self.head.pos[1] + 1:
                re[3] = 1 
        # print(re)
        return re

    def move(self, dis, brain):
        if brain:
            self.move_with_brain(dis, brain)
        else:
            self.move_with_keys()
                
        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)
    
    def clear_scores(self):
        self.score.clear()
        self.deaths = 0
        self.avg_steps.clear()
        self.penalities.clear()

    def play(self, dis = True, brain = None):
        self.clear_scores()
        if dis:
            screen = pygame.display.set_mode((width, width))
            clock = pygame.time.Clock()
        self.food = cube(randomfood(rows, self), color=(0,255,0))

        steps = 0
        penality = 0
        tmp = 0
        while steps < 500:
            # pygame.time.delay(50)
            # clock.tick(2)
            self.move(dis, brain)

            if self.body[0].pos == self.food.pos:
                self.addCube()
                self.food = cube(randomfood(rows, self), color=(0,255,0))

                self.avg_steps.append(tmp)
                if tmp>20:
                    penality+=1
                tmp = 0
            tmp += 1
            

            f = 0
            if self.body[0].dirnx == -1 and self.body[0].pos[0]<0:
                f = 1
            elif self.body[0].dirnx == 1 and self.body[0].pos[0]>rows-1:
                f = 1
            elif self.body[0].dirny == 1 and self.body[0].pos[1]>rows-1:
                f = 1
            elif self.body[0].dirny == -1 and self.body[0].pos[1]<0:
                f = 1
            if f == 1:
                self.score.append(len(self.body))
                self.penalities.append(penality)
                self.deaths += 1
                penality = 0
                tmp = 0
                self.reset((10,10))
            else:
                for x in range(1,len(self.body)):
                    if self.body[0].pos == self.body[x].pos:
                        self.score.append(len(self.body))
                        self.penalities.append(penality)
                        self.deaths += 1
                        penality = 0
                        tmp = 0
                        self.reset((10,10))
                        break
            if dis:
                self.redrawWindow(screen, width, rows, self.food)
            steps+=1
        self.reset((10,10))

    def fitness_fun(self):
        avg = 0
        if len(self.avg_steps) != 0:
            avg = sum(self.avg_steps)/len(self.avg_steps)
        if len(self.score) == 0:
            self.score.append(1)
        val = (max(self.score))*5000 - 150 * self.deaths - 100 * avg - 1000 * sum(self.penalities
        )
        return self.score, max(self.score), self.deaths, avg, self.penalities, val

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface)
    
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        self.body.append(cube((tail.pos[0]-dx, tail.pos[1]-dy)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def reset(self, pos):
        self.body = []
        self.head = cube(pos)
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.food = cube(randomfood(rows, self), color=(0,255,0))


    def redrawWindow(self, surface, width, rows, food):
        surface.fill((0,0,0))
        drawGrid(surface, width, rows)
        self.draw(surface)
        food.draw(surface)
        pygame.display.update()

def drawGrid(surface, w, rows):
    sizeBtwn = w//rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x, 0), (x,w))
        pygame.draw.line(surface, (255,255,255), (0, y), (w,y))


def randomfood(rows, eater):
    positions = eater.body
    while 1:
        x = random.randrange(rows)
        y = random.randrange(rows)
        f = 0
        for c in positions:
            if c.pos == (x,y):
                f = 1
        if f: continue
        else: break
    return (x,y)

def main():
    global width, rows
    width = 500
    rows = 20

    # b = neural_network()
    # s = snake((255,0,0),(10,10))
    # s.play(1, b)
    # print(s.fitness_fun())
    
    # b.forward_prop([1,1,1,1,1,1,1,1,1,1,1,1])

main()