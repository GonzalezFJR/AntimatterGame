"""
  Class particle 
  This contains particle type and properties, kinematics and drawing options
  Question: maybe we can add an inplementation to represent a particle as an orbital - in case we want to represent atoms or any bound states (positronium?)
"""

class particle:

  def __init__(self, pclass, x0, y0, vx0, vy0, mass=1, charge=1, name='electron'):
    self.InitParticle()
    self.InitState(x0, y0, vx0, vy0)

  def InitParticle(self, pclass, mass=1, charge=1, name='electron'):
    self.SetClass(pclass)
    self.SetCharge(charge)
    self.SetMass(mass)
    self.SetName(name)

  def InitState(x0=0, y0=0, vx0=0, vy0=0):
    self.x = x0
    self.y = y0
    self.vx = vx0
    self.vy = vy0

  ### Kinematics
  ########################################################

  def SetPos(self, x, y):
    self.x = x
    self.y = y

  def SetVel(self, vx, vy):
    self.xy = vx
    self.vy = vy

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

  def SetRadiut(self, rad):
    self.radius = rad

