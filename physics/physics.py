"""
  Class that implement interaction between particles and fields
  Particles can interact with fields and update it momentum and position
  Particles can be anihilated with other particles
"""

import os, sys
import random, math
### Set the base path of the repository
basepath = os.path.abspath(__file__).rsplit('/AntimatterGame/',1)[0]+'/AntimatterGame/'
sys.path.append(basepath)
sys.path.append(basepath+'physics/')

from physics.field import field, magneticField, electricField, fieldType
from physics.particle import *
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
    self.SetBorders(do=False, width=4)
    self.interactionRadius = 0.15
    self.photonSpeed = 4

  def Reset(self):
    """ Set fields to zero. Remove all particles. """
    self.magneticField = magneticField()
    self.electricField = electricField()
    self.particles.clear()
    #self.SetTimeInterval()
    
  ### Evolution and matematics
  #################################################

  def Scatter(self, p1, p2):
    """ Scatter particles. We can add multiple interactions here """
    cpro = p1.charge*p2.charge
    if p1.pclass == p2.pclass or cpro == 1:
      return self.ScatterPartilces(p1, p2)
    elif cpro==-1:
      return self.Anihilate(p1, p2)

  def Anihilate(self, p1, p2):
    """ Create two photons with random opposite directions and add them """
    x = (p1.x+p2.x)/2
    y = (p1.y+p2.y)/2
    angle = random.uniform(0, 2*3.141592)
    vx = self.photonSpeed*math.sin(angle)
    vy = self.photonSpeed*math.cos(angle)
    photon1 = NewParticle('photon',x,y,vx,vy)
    photon2 = NewParticle('photon',x,y,-vx,-vy)
    return [photon1, photon2]

  def ScatterPartilces(self, p1, p2):
    pass

  def Update(self):
    """ Update the status of the universe """
    for p in self.particles:
      # First update positions according to their velocities
      # p.UpdatePosition(self.dt)
      # Then update velocities according to fields
      #vx, vy, vz = self.UpdateParticleVelocity(p)
      x, v = self.UpdateParticleVelocityAndPosition(p)
      p.SetPos(x)
      p.SetVel(v)
    return self.CheckDynamics()

  def SetTimeInterval(self, dt=0.01):
    self.dt = dt

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

  def CheckDynamics(self):
    """ Checks the position of the particles and performs dynamics """
    removeIndices = []
    for i in range(len(self.particles)):
      if self.doBorders and self.particles[i].charge != 0:
        if abs(self.particles[i].x) > abs(self.width ): 
          self.particles[i].vx *= -1
          self.particles[i].x = self.width if self.particles[i].x > self.width else -self.width
        if abs(self.particles[i].y) > abs(self.height): 
          d = self.height-self.particles[i].y
          self.particles[i].vy *= -1
          self.particles[i].y = self.height if self.particles[i].y > self.height else -self.height
      else:
        if   abs(self.particles[i].x) > abs(self.width )*1.5: removeIndices.append(i)
        elif abs(self.particles[i].y) > abs(self.height)*1.5: removeIndices.append(i)
      for j in range(i):
        if self.particles[i].GetDistance(self.particles[j]) <= self.interactionRadius:
          scatter = self.Scatter(self.particles[i], self.particles[j])
          if isinstance(scatter, list) and len(scatter) == 2:
            for f in scatter: self.AddParticle(f)
            removeIndices.append(i)
            removeIndices.append(j)
          else: # They are scattering elastically
            pass
    # Remove particles
    for i in sorted(removeIndices, reverse=True): del self.particles[i]
    return len(removeIndices) != 0

  ### Set methods
  ##################################################
  def AddParticle(self, part):
    self.particles.append(part)

  def SetMagneticField(self, mag):
    if isinstance(mag, magneticField): self.magneticField = magField
    else: 
      # I assume this is a magnitud and direction in z axis
      self.magneticField.SetZfield(mag)

  def SetElectricField(self, x=None, y=None):
    if isinstance(x, electricField): self.electricField = x
    elif y == None: self.electricField.SetHorizontal(x)
    elif x == None: self.electricField.SetVertical(y)
    else: self.electricField.SetField(x,y)

  def SetBorders(self, do=True, width=4, height=None):
    self.doBorders = do
    self.width = width
    self.height = height if not height is None else width

  def SetInteractionRadius(self, r):
    self.interactionRadius = r

  def SetPhtonSpeed(self, speed=2):
    self.photonSpeed = speed

  def GetParticles(self):
    ''' Return particles to be drawn... '''
    return self.particles

  ########################################################

  def CreateRandomParticles(self, n, name, maxSpeed=1):
    for i in range(n):
      x = random.uniform(-self.width, self.width)
      y = random.uniform(-self.height, self.height)
      vx = random.uniform(-maxSpeed, maxSpeed)
      vy = random.uniform(-maxSpeed, maxSpeed)
      self.AddParticle(NewParticle(name, x, y, vx, vy))

  def CreateRandomEE(self, nElectrons, nPositrons=None, maxSpeed=1):
    if nPositrons == None: nPositrons = nElectrons
    self.CreateRandomParticles(nElectrons, 'electron', maxSpeed)
    self.CreateRandomParticles(nPositrons, 'positron', maxSpeed)
