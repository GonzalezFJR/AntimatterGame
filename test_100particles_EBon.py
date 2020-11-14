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
myUniverse.CreateRandomEE(50)
myUniverse.SetTimeInterval(0.05)
myUniverse.SetBorders(1, width=width)

aa = antimatterAnimation(myUniverse, width=width, savename='test')
aa.draw()
