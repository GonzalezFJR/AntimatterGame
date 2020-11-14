"""
  Class particle 
  This contains particle type and properties, kinematics and drawing options
  Question: maybe we can add an inplementation to represent a particle as an orbital - in case we want to represent atoms or any bound states (positronium?)
"""

class particle:

  def __init__(self, pclass, x0, y0, vx0, vy0, mass=1, charge=1, name='electron', color='b'):
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

  def SetPos(self, x, y, z=0):
    self.x = x
    self.y = y
    self.z = z

  def SetVel(self, vx, vy, vz=0):
    self.vy = vx
    self.vy = vy
    self.vz = vz

  def GetVel(self):
    return [self.vx, self.vy, self.vz]

  def GetPos(self):
    return [self.x, self.y, self.z]

  def UpdatePosition(self, dt=1):
    x = self.x + self.vx*dt
    y = self.y + self.vy*dt
    z = self.x + self.vz*dt
    self.SetPos(x,y,z)

  ### Properties
  ########################################################
  def SetCharge(self, charge=1):
    """ Charge in units of e charge """
    self.charge = 1

  def SetMass(self, mass=1):
    """ Mass in units of e mass (0.511 MeV) """
    self.mass = 1

  def SetClass(self, c=1):
    """ c=1 if matter, c=-1 if antimatter """
    self.c = c

  def SetName(self, name):
    self.name = name

  def IsMatter(self):
    return self.c == 1

  def IsAntimatter(self):
    return self.c != 1

  def GetName(self):
    return self.name

  ### Drawing...
  ########################################################
  def SetColor(self, color):
    self.color = color

  def SetRadius(self, rad):
    self.radius = rad
