
from boat import Boat
from environment import Race
import loggingFunc
import numpy as np
import pygame

raceVar = Race(np.pi)
boatA = Boat([400,400],sim=False)
# boatA.vel[0] = 100

# logger = loggingFunc.logSim()

updateRate = 60
dt = 1.0/updateRate

WIDTH, HEIGHT =  1800, 1200
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sailing Sim")

boats = [boatA]

run = True
clock = pygame.time.Clock()
ctr = 0

while run:
    clock.tick(updateRate)
    WIN.fill(BLUE)

    # ctr += 1
    # if ctr >= 1:
    #     run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for boat in boats:
        boat.update(raceVar, dt)
        boat.draw(WIN)

    raceVar.draw(WIN)

    boatA.updateInput(pygame.key.get_pressed())
    
    pygame.display.update()

    # logTemp = [t, boatA.pos, boatA.vel, boatB.pos, boatB.vel]
    # logger.log(logTemp)

# print(logger.vars[0].var)
