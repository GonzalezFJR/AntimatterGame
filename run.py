from physics.field    import field, magneticField, electricField, fieldType
from physics.particle import *
from physics.physics  import physics
from plotter.antimatterAnimation import antimatterAnimation

### Create an electric and magnetif field
#B = magneticField(2)
#E = electricField(1.,0.)

### You can add particles by hand
#myUniverse.AddParticle(NewParticle('electron', 0, 0, 0.5, 0.5))
#myUniverse.AddParticle(NewParticle('electron', 1, 0, 0.0, 0.5))
#myUniverse.AddParticle(NewParticle('positron', 1, 1, 0.4, 0.5))
#myUniverse.AddParticle(NewParticle('electron', 0.3,  0, -0.4, 0.))
#myUniverse.AddParticle(NewParticle('positron', -0.3, 0, -0.4, 0.))
#myUniverse.AddParticle(NewParticle('positron', 0, 1, 0.4, 0.0))

### Or create plenty of particles with random velocities
#myUniverse.CreateRandomEE(55, 50)


width = 3
myUniverse = physics()
myUniverse.SetTimeInterval(0.05)
myUniverse.SetBorders(1, width=width)

animation = antimatterAnimation(myUniverse, width=width)
animation.draw()
