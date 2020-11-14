from physics.field    import field, magneticField, electricField, fieldType
from physics.particle import particle
from physics.physics  import physics
from plotter.antimatterAnimation import antimatterAnimation as AA

B = magneticField(2)
E = electricField(0.,0.)
electron = particle(1,  x0=0,   y0=0,   vx0=0, vy0=0.5, mass=1, charge=-1, color='b')
positron = particle(-1, x0=0.5, y0=0.5, vx0=0, vy0=0.5, mass=1, charge= 1, color='r')
myUniverse = physics(B, E, electron, positron)
myUniverse.SetTimeInterval(0.01)

aa = AA(myUniverse)
aa.draw()
