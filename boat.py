
import numpy as np

class boat():
      
    C_d = 0.5
    C_h = 1
    PID_heading = [1,0,0]
    PID_sail = [1,0,0]

    def __init__(self,pos):
        
        self.pos = np.array(pos)
        self.vel = 0
        
        # Heading Params
        self.heading = 0
        self.rudder = 0

        # Sail Params
        self.trim = 0
        self.trim_power = 0.5

        self.theta_wind_B = 0
        
    
    def setSteering(self, environment, dt):
        self.rudder = 0

    def setSails(self, environment, dt):
        self.theta_wind_B = self.heading - environment.theta_wind
        if (self.theta_wind_B):
            pass

    def updateModel(self, environment, dt):

        self.vel = self.C_d * environment.wind_vel * self.trim_power
        
        self.heading = self.heading + self.C_h * (self.rudder * self.vel) * dt
        
        self.pos = self.pos + (self.vel * np.array([np.cos(self.heading), np.sin(self.heading)]) * dt)

        

    def update(self,environment, dt):

        self.setSteering(environment, dt)
        
        self.setSails(environment, dt)

        self.updateModel(environment, dt)
