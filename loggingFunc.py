
import os
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt


class logVar():
    def __init__(self,name='VarName'):
        self.name = name
        self.var = np.array([])

    def log(self,var):
        self.var = np.append(self.var,var)


class logArr():
    def __init__(self,name='VarName'):
        self.name = name
        self.var = None

    def log(self,var):
        if self.var is None:
            self.var = var
        else:
            self.var = np.vstack((self.var, var))

class logSim():
    def __init__(self):
        self.vars = None

    def log(self,Vars):
        if self.vars is None:
            self.vars = []
            for var in Vars:
                if type(var) == np.ndarray:
                    self.vars.append(logArr())
                else:
                    self.vars.append(logVar())
        for k in range(len(Vars)):
            self.vars[k].log(Vars[k])


def plotVar(var):
    plt.plot(np.arange(var.shape[0]), var)
    plt.xlabel('Index')
    plt.ylabel('Var')
    plt.grid()

def plot2Var(var1,var2):
    plt.plot(var1, var2)
    plt.xlabel('Var1')
    plt.ylabel('Var2')
    plt.grid()
