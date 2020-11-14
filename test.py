from physics.field    import field, magneticField, electricField, fieldType
from physics.particle import particle
from physics.physics  import physics
from plotter.antimatterAnimation import antimatterAnimation as AA

B = magneticField(0.6)
E = electricField(0.,0.1,0)
electron = particle(1,  0,   0,   0, 0.05, mass=1, charge=-1, color='b')
positron = particle(-1, 0.5, 0.5, 0.05, 0, mass=1, charge=1,  color='r')
myUniverse = physics(B, E, electron, positron)
myUniverse.SetTimeInterval(0.01)

aa = AA(myUniverse)
aa.draw()
