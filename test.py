from physics.field    import field, magneticField, electricField, fieldType
from physics.particle import *
from physics.physics  import physics
from plotter.antimatterAnimation import antimatterAnimation

width = 3
B = magneticField(2)
E = electricField(1.,0.)
#electron = particle(1,  x0=0,   y0=0,   vx0=0, vy0=0.5, mass=1, charge=-1, color='b')
#positron = particle(-1, x0=0.5,  y0=0.5, vx0=0, vy0=0.5, mass=1, charge= 1, color='r')
myUniverse = physics(B, E)
myUniverse.AddParticle(NewParticle('electron', 0, 0, 0.5, 0.5))
myUniverse.AddParticle(NewParticle('electron', 1, 0, 0.0, 0.5))
myUniverse.AddParticle(NewParticle('positron', 1, 1, 0.4, 0.5))
myUniverse.AddParticle(NewParticle('electron', 0.3,  0, -0.4, 0.))
myUniverse.AddParticle(NewParticle('positron', -0.3, 0, -0.4, 0.))
myUniverse.AddParticle(NewParticle('positron', 0, 1, 0.4, 0.0))

#myUniverse.CreateRandomEE(40)
myUniverse.SetTimeInterval(0.05)
myUniverse.SetBorders(1, width=width)

aa = antimatterAnimation(myUniverse, width=width, savename='test')
aa.draw()
