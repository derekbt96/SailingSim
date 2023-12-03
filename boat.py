
import numpy as np
import pygame

class Boat():
      
    C_d_water = (0.2,4.0)
    C_d_air = 0.005
    C_h = 0.1
    M = 100.0
    I = 2.0
    Fmax = 15

    PID_heading = [1,0,0]
    PID_sail = [1,0,0]
    SCALE = 15
    boat_points = np.array([(1,0), (0,0.4), (-1,0.3), (-1,-0.3), (0,-0.4)])
    sail_points = np.array([(0,0), (-0.8,0)])

    def __init__(self,pos,color=(255, 255, 255),sim=True):
        
        self.pos = np.array(pos)
        self.vel = np.array([0.0,0.0])
        
        self.sim = sim

        # Heading Params
        self.heading = np.pi / 4.0
        self.rudder = 0.0

        # Sail Params
        self.trim = 25 * np.pi / 180.0
        self.sail_theta = self.trim
        self.trim_vec = np.array([np.cos(self.sail_theta),np.sin(self.sail_theta)])
        self.trim_power = 0.5
        self.plotvec1 = None
        self.plotvec2 = None
        self.plotvec3 = None
        
        self.color = color
        
        
    def updateInput(self,keys):
        if keys[pygame.K_LEFT]:
            self.rudder -= 0.01
        elif keys[pygame.K_RIGHT]:
            self.rudder += 0.01
        elif abs(self.rudder) >= 0.01:
            self.rudder -= np.sign(self.rudder) * 0.01
        else:
            self.rudder = 0
        if (abs(self.rudder) > 0.5):
            self.rudder = np.sign(self.rudder)*0.5
        

    def setSteering(self, environment, dt):
        self.rudder = 0

    def setSails(self, environment, dt):

        self.theta_wind_B = self.contrain_theta(self.heading - environment.wind_theta)
        if abs(self.theta_wind_B) > (155 * (np.pi/180)):
            self.sail_theta = -np.sign(self.theta_wind_B) * (np.pi/2 - (np.pi - abs(self.theta_wind_B)))
        else:
            # self.sail_theta = -np.sign(self.theta_wind_B) * (np.pi/2 - self.trim)
            self.sail_theta = -np.sign(self.theta_wind_B) * (abs(self.theta_wind_B) / 2)
        self.trim_vec = np.array([np.cos(self.sail_theta), np.sin(self.sail_theta)])

    def updateModel(self, environment, dt):

        

        Rf2bdy = np.array([[np.cos(self.heading),np.sin(self.heading)],
                           [-np.sin(self.heading),np.cos(self.heading)]])
        Rbdy2f = np.transpose(Rf2bdy)
        V_wind_bdy = np.matmul(Rf2bdy, (environment.wind_vel - self.vel))
        V_water_bdy = np.matmul(Rf2bdy, (environment.current - self.vel))

        # Drag Water
        force_bdy = np.multiply(V_water_bdy,self.C_d_water)
        f_drag_water = np.matmul(Rbdy2f, force_bdy)
        force = f_drag_water

        # Drag Air
        f_drag_air = -(self.vel) * self.C_d_air
        force += f_drag_air

        # Sail Power
        f_sail_bdy = self.trim_power * (np.dot(V_wind_bdy,self.trim_vec) * self.trim_vec)
        f_sail_f = np.matmul(Rbdy2f, f_sail_bdy)
        if (np.linalg.norm(f_sail_f) > self.Fmax):
            f_sail_f = f_sail_f *  (self.Fmax / np.linalg.norm(f_sail_f))
        force += f_sail_f

        self.plotvec1 = f_sail_f
        self.plotvec2 = force

        # Update velocity
        self.vel += force / self.M
        self.plotvec3 = self.vel / 3
        
        # Update Heading
        d_heading = self.C_h * (self.rudder * np.linalg.norm(V_water_bdy) * -np.sign(V_water_bdy[0]))
        self.heading = self.contrain_theta(self.heading + d_heading * dt)
        
        self.pos = self.pos + (self.vel * dt)
        # print(self.pos)


    def draw(self, win):

        C = np.array([[np.cos(self.heading),np.sin(self.heading)],
                      [-np.sin(self.heading),np.cos(self.heading)]])
        updated_points = self.SCALE * np.matmul(self.boat_points, C) + self.pos
        pygame.draw.lines(win, (255,255,255), True, updated_points, 1)
        pygame.draw.circle(win, self.color, self.pos, self.SCALE/4)

        if not self.sim:
            rudder_points = np.array([[self.rudder*50+400,50],[400,50]])
            pygame.draw.lines(win, (188, 39, 50), False, rudder_points, 5)

        sail_points = self.SCALE * np.matmul(np.array([[0,0],[-np.cos(np.pi/2 - abs(self.sail_theta)),np.sign(self.sail_theta)*np.cos(self.sail_theta)]]), C) + self.pos
        pygame.draw.lines(win, (255,255,255), True, sail_points, 2)
        # print([-np.cos(self.trim),np.sign(self.sail_theta)*np.sin(self.trim)])
        
        if self.plotvec1 is not None:
            force_points1 = self.SCALE * np.array([[0,0],self.plotvec1]) + self.pos
            pygame.draw.lines(win, (188, 39, 50), True, force_points1, 2)
        if self.plotvec2 is not None:
            force_points2 = self.SCALE * np.array([[0,0],self.plotvec2]) + self.pos
            pygame.draw.lines(win, (255, 255, 0), True, force_points2, 2)
        if self.plotvec3 is not None:
            force_points3 = self.SCALE * np.array([[0,0],self.plotvec3]) + self.pos
            pygame.draw.lines(win, (80, 78, 81), True, force_points3, 2)


    def update(self,environment, dt):

        # self.setSteering(environment, dt)
        
        self.setSails(environment, dt)

        self.updateModel(environment, dt)

    def contrain_theta(self,inVar):
        if inVar > np.pi:
            return inVar - 2*np.pi
        elif inVar < -np.pi:
            return inVar + 2*np.pi
        else:
            return inVar
