'''
  This is a class that takes a list of particle and draws all the positions
  and gets updated each time interval
'''

import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as ani
import os
import subprocess


class antimatterAnimation:

  def __init__(self, universe, width=4):
    self.fig, self.ax = plt.subplots()
    self.universe = universe
    self.text = ''
    self.plots = []
    for p in self.universe.GetParticles(): 
      self.plots.append(self.ax.plot([], [],'o',color = p.color))
    self.width = width
    self.height= self.width
    
  ################################################
  ################################################

  def update(self, i):
    self.universe.Update()
    values = []
    ipart = 0
    for p in self.universe.GetParticles():
      self.plots[ipart][0].set_data(p.x, p.y); 
      values.append(self.plots[ipart][0])        
      ipart+=1
    #text.set_text('test')
    #values.append(text)
    return values

  def draw(self):
    particles = self.universe.GetParticles()
    self.ax.set(xlabel='x', ylabel='y', title='Antimatter game', xlim=(-5,5), ylim=(-5,5))
    self.ax.set_ylim(-self.width, self.width)
    self.ax.set_xlim(-self.height,self.height)
    #text = ax.text(-tam+0.1*tam, tam-0.1*tam,'')#, transform=spl.transAxes)

    def init():
      """ Initializing function """
      #text.set_text('')
      values = []
      for j in range(len(universe.GetParticles())):
        self.plots[j][0].set_data([], []); 
        values.append(self.plots[j][0])
      return values

    universe = self.universe
    anim = ani.FuncAnimation(self.fig,self.update,init_func=init, frames=(1000000), interval=10, blit=True)
    print("Drawing...")
    plt.show()
    #ani.save('animation.mp4', fps=100, dpi=300)
    return anim

