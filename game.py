import random
import pygame
import numpy as np
from test import neural_network

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

    def move_with_brain(self):
        inp = self.get_surroundings()
        x = b.forward_prop(inp)
        print(x[0])
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
        return [1,1,1,1,1,1,1,1,1,1,1,0]

    def move(self):
        self.move_with_brain()
                
        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0]<=0:
                    c.pos = (rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0]>=rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1]>=rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1]<=0:
                    c.pos = (c.pos[0], rows-1)
                else:
                    c.move(c.dirnx, c.dirny)
    
    def play(self):
        screen = pygame.display.set_mode((width, width))
        food = cube(randomfood(rows, self), color=(0,255,0))
        clock = pygame.time.Clock()

        flag = 0
        tmp = 0
        penality = 0
        while flag < 3:
            pygame.time.delay(50)
            clock.tick(10)
            self.move()

            if self.body[0].pos == food.pos:
                self.addCube()
                food = cube(randomfood(rows, self), color=(0,255,0))

                self.avg_steps.append(tmp)
                if tmp > 30:
                    penality+=1
                tmp = 0
            tmp+=1

            for x in range(1,len(self.body)):
                if self.body[0].pos == self.body[x].pos:
                    self.score.append(len(self.body))
                    self.penalities.append(penality)
                    penality = 0
                    self.reset((10,10))
                    flag += 1
                    break
            self.redrawWindow(screen, width, rows, food)

    def fitness_fun(self):
        val = max(self.score)*5000 - 150 * sum(self.avg_steps)/len(self.avg_steps) - 100 * sum(self.penalities
        )
        return self.score, sum(self.avg_steps)/len(self.avg_steps), self.penalities, val

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
    global width, rows, b
    width = 500
    rows = 20

    b = neural_network()
    s = snake((255,0,0),(10,10))
    s.play()
    # print(s.fitness_fun())
    
    # b.forward_prop([1,1,1,1,1,1,1,1,1,1,1,1])

main()