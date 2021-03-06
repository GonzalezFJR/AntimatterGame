"""
  Class particle 
  This contains particle type and properties, kinematics and drawing options
  Question: maybe we can add an inplementation to represent a particle as an orbital - in case we want to represent atoms or any bound states (positronium?)
"""

import numpy as np

class particle:

  def __init__(self, pclass, x0=0, y0=0, vx0=0, vy0=0, mass=1, charge=1, name='electron', color='b'):
    self.InitParticle(pclass, mass, charge, name)
    self.InitState(x0, y0, vx0, vy0)
    self.SetColor(color)

  def InitParticle(self, pclass, mass=1, charge=1, name='electron'):
    self.SetClass(pclass)
    self.SetCharge(charge)
    self.SetMass(mass)
    self.SetName(name)

  def InitState(self, x0=0, y0=0, vx0=0, vy0=0):
    self.x = x0
    self.y = y0
    self.z = 0
    self.vx = vx0
    self.vy = vy0
    self.vz = 0

  ### Kinematics
  ########################################################

  def SetPos(self, x, y=0, z=0):
    if isinstance(x, list) or isinstance(x, np.ndarray):
      x,y,z = x
    self.x = x
    self.y = y
    self.z = z

  def SetVel(self, vx, vy=0, vz=0):
    if isinstance(vx, list) or isinstance(vx, np.ndarray): 
      vx,vy,vz = vx
    self.vx = vx
    self.vy = vy
    self.vz = vz

  def GetVel(self):
    return [self.vx, self.vy, self.vz]

  def GetPos(self):
    return [self.x, self.y, self.z]

  def UpdatePosition(self, dt=0.1):
    x = self.x + self.vx*dt
    y = self.y + self.vy*dt
    z = self.x + self.vz*dt
    self.SetPos(x,y,z)

  def GetDistance(self, p):
    dx = self.x - p.x
    dy = self.y - p.y
    return np.sqrt(dx*dx + dy*dy)

  ### Properties
  ########################################################
  def SetCharge(self, charge=1):
    """ Charge in units of e charge """
    self.charge = charge

  def SetMass(self, mass=1):
    """ Mass in units of e mass (0.511 MeV) """
    self.mass = 1

  def SetClass(self, c=1):
    """ c=1 if matter, c=-1 if antimatter """
    self.pclass = c

  def SetName(self, name):
    self.name = name

  def IsMatter(self):
    return self.pclass == 1

  def IsAntimatter(self):
    return self.pclass != 1

  def GetName(self):
    return self.name

  ### Drawing...
  ########################################################
  def SetColor(self, color):
    self.color = color

  def SetRadius(self, rad):
    self.radius = rad

def Electron(x0=0, y0=0, vx0=0, vy0=0, color=None):
  return particle(1, x0, y0, vx0, vy0, mass=1, charge=-1, name='electron', color=color if not color is None else 'b')

def Positron(x0=0, y0=0, vx0=0, vy0=0, color=None):
  return particle(-1, x0, y0, vx0, vy0, mass=1, charge= 1, name='positron', color=color if not color is None else 'r')

def Photon(x0=0, y0=0, vx0=0, vy0=0, color=None):
  return particle(1, x0, y0, vx0, vy0, mass=1, charge= 0, name='photon', color='k')

def NewParticle(name='electron', x0=0, y0=0, vx0=0, vy0=0, color=None):
  if   name=='electron': return Electron(x0, y0, vx0, vy0, color)
  elif name=='positron': return Positron(x0, y0, vx0, vy0, color)
  elif name=='photon'  : return Photon  (x0, y0, vx0, vy0, color)
  else:
    print("ERROR: particle '%s' not yet implemented... "%name)
