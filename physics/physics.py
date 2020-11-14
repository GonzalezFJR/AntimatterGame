"""
  Class that implement interaction between particles and fields
  Particles can interact with fields and update it momentum and position
  Particles can be anihilated with other particles
"""

import os, sys
### Set the base path of the repository
basepath = os.path.abspath(__file__).rsplit('/AntimatterGame/',1)[0]+'/AntimatterGame/'
sys.path.append(basepath)
sys.path.append(basepath+'physics/')

from physics.field import field, magneticField, electricField, fieldType
from physics.particle import particle
from physics.Boris import GetNextWithBoris

class physics:
  def __init__(self, *objects):
    self.magneticField = None
    self.electricField = None
    self.particles = []
    self.Reset() # Set everything to zero
    for o in objects:
      if   isinstance(o, particle):      self.AddParticle(o)
      elif isinstance(o, magneticField): self.magneticField = o
      elif isinstance(o, electricField): self.electricField = o
      else: print("WARNING -- unknown object : ", o)

  def Reset(self):
    """ Set fields to zero. Remove all particles. """
    self.magneticField = magneticField()
    self.electricField = electricField()
    self.particles.clear()
    self.SetTimeInterval()
    self.SetNsteps(1)
    
  ### Evolution and matematics
  #################################################

  def CheckAnihilation(self):
    pass

  def CreatePhotons(self):
    pass

  def Update(self):
    for p in self.particles:
      # First update positions according to their velocities
      # p.UpdatePosition(self.dt)
      # Then update velocities according to fields
      #vx, vy, vz = self.UpdateParticleVelocity(p)
      x, v = self.UpdateParticleVelocityAndPosition(p)
      p.SetPos(x)
      p.SetVel(v)

  def SetTimeInterval(self, dt=0.01):
    self.dt = dt

  def SetNsteps(self, n=100):
    self.nSteps = n

  def UpdateParticleVelocity(self, p):
    """ For the moment, for a uniform field... 
        This is old... not use it!
    """
    q = p.charge; m = p.mass
    vx0, vy0, vz0 = p.GetVel()
    bx,  by,  bz  = self.magneticField.Get()
    ex,  ey,  ez  = self.electricField.Get()
    ### Acceleration caused by the magnetic field
    ax = (vy0*bz - vz0*by)*q/m
    ay = (vz0*bx - vx0*bz)*q/m
    az = (vx0*by - vy0*bx)*q/m
    ### Acceleration caused by the electric field
    ax += q*ex
    ay += q*ey
    az += q*ez
    ### New velocities
    vx = vx0 + ax*self.dt
    vy = vy0 + ay*self.dt
    vz = vz0 + az*self.dt
    ### Update velocities
    return vx, vy, vz

  def UpdateParticleVelocityAndPosition(self, p):
    v = p.GetVel(); x = p.GetPos()
    B = self.magneticField.Get()
    E = self.electricField.Get()
    x, v = GetNextWithBoris(self.dt, x, v, B, E, mass=p.mass, charge=p.charge)
    return x, v

  ### Set methods
  ##################################################
  def AddParticle(self, part):
    self.particles.append(part)

  def SetMagneticField(self, mag):
    if isintance(mag, magneticField): self.magneticField = magField
    else: 
      # I assume this is a magnitud and direction in z axis
      self.magneticField.SetZfield(mag)

  def SetElecticField(self, x=None, y=None):
    if isinstance(x, electricField): self.electricField = x
    elif y == None: self.electricField.SetHorizontal(x)
    elif x == None: self.electricField.SetVertical(y)
    else: self.electricField.SetField(x,y)

  ### Drawing options
  ##################################################

  def GetParticles(self):
    ''' Return particles to be drawn... '''
    return self.particles
