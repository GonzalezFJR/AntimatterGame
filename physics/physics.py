"""
  Class that implement interaction between particles and fields
  Particles can interact with fields and update it momentum and position
  Particles can be anihilated with other particles
"""

class physics(self, *objects):
  self.magneticField = None
  self.electricField = None
  self.particles = []

  def Initialize(self):
    pass

  def Reset(self):
    pass

  ### Evolution and matematics
  #################################################

  def CheckAnihilation(self):
    pass

  def CreatePhotons(self):
    pass

  def Update(self):
    pass

  def SetTimeInterval(self, dt=0.01):
    self.dt = dt

  def SetNsteps(self, n=100):
    self.nSteps = n

  ### Set methods
  ##################################################
  def SetMagneticField(self, *values):
    pass

  def SetElectricField(self, field):
    pass

  def AddParticle(self, part):
    self.particles.append(part)

  ### Drawing options
  ##################################################

