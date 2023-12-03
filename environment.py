
import numpy as np
import pygame

class Race():
      
    arrow_points = np.array([(-2,0), (1,0), (0,1), (0,-1), (1,0)])
    SCALE = 30
    draw_pos = np.array([50.50])

    def __init__(self,theta_wind_nom):
        self.wind_vel = np.array([50,0])
        self.wind_vel_nom = theta_wind_nom
        self.current = np.array([0,0])
        self.wind_theta = np.arctan2(self.wind_vel[1],self.wind_vel[0])
    
    def draw(self,win):
        C = np.array([[np.cos(self.wind_theta),np.sin(self.wind_theta)],
                      [-np.sin(self.wind_theta),np.cos(self.wind_theta)]])
        updated_points = self.SCALE * np.matmul(self.arrow_points, C) + self.draw_pos
        pygame.draw.lines(win, (255,255,255), True, updated_points, 10)
    
    def updateModel(self, environment):
        # self.theta_wind = 0
        pass