
from boat import boat
from environment import race
import loggingFunc
import numpy as np
import pygame

raceVar = race(np.pi)
boatA = boat([0,0])
boatB = boat([10,0])

logger = loggingFunc.logSim()

dt = 0.1
t = 0

a = 1.0
b = np.array([1,2,3])


for i in range(100):

    raceVar.updateModel(dt)

    boatA.update(raceVar,dt)
    boatB.update(raceVar,dt)

    logTemp = [t, boatA.pos, boatA.vel, boatB.pos, boatB.vel]
    logger.log(logTemp)
    
    t += dt

print(logger.vars[0].var)
