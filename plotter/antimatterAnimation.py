'''
  This is a class that takes a list of particle and draws all the positions
  and gets updated each time interval
'''

import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as ani
import os, sys, random
import subprocess

basepath = os.path.abspath(__file__).rsplit('/AntimatterGame/',1)[0]+'/AntimatterGame/'
sys.path.append(basepath)
sys.path.append(basepath+'physics/')
from physics.particle import *
from matplotlib.widgets import Slider, Button, RadioButtons

axcolor = 'lightgoldenrodyellow'


class antimatterAnimation:

  def __init__(self, universe, width=4, savename=None):
    self.fig, self.ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9)
    self.universe = universe
    self.text = ''
    self.plots = []
    self.partmode = 'electron'
    self.savename = savename
    for p in self.universe.GetParticles(): 
      self.plots.append(self.ax.plot([], [],'o',color = p.color, fillstyle='none' if p.color=='k' else 'full'))
    self.width = width
    self.height= self.width
    
    #on_press event
    def on_press(event):
      #print('you pressed', event.button, event.xdata, event.ydata)
      vx = random.uniform(-1,1)
      vy = random.uniform(-1,1)
      if event.xdata == 0 and event.ydata == 0: return
      if event.xdata is None: return
      if abs(event.xdata) > self.width or abs(event.ydata) > self.height: return
      self.universe.AddParticle(NewParticle(self.partmode, event.xdata, event.ydata, vx, vy))
      self.mod = True
    cid = self.fig.canvas.mpl_connect('button_press_event', on_press)

    resetax = plt.axes([0.77, 0.025, 0.14, 0.04])
    self.button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    rax = plt.axes([0.77, 0.068, 0.14, 0.15], facecolor=axcolor)
    self.particleSelector = RadioButtons(rax, ('electron', 'positron'), active=0)

    axmag  = plt.axes([0.25, 0.1, 0.45, 0.03], facecolor=axcolor)
    axelec = plt.axes([0.25, 0.15,0.45, 0.03], facecolor=axcolor)

    self.magFieldSlider  = Slider(axmag,  'Magnetic field', -1., 1.0, valinit=0)#, valstep=delta_f)
    self.elecFieldSlider = Slider(axelec, 'Electric field', -1., 1.0, valinit=0)

    
  ################################################
  ################################################


  def update(self, i):
    mod = self.universe.Update()
    values = []
    ipart = 0
    #print('len(self.universe.GetParticles()) = ', len(self.universe.GetParticles()))
    prevPart = len(self.plots)
    for p in self.universe.GetParticles():
      if ipart >= prevPart: 
        self.plots.append(self.ax.plot([], [],'o',color = p.color, fillstyle=('none' if p.color=='k' else 'full') ))
      # Set color and style
      self.plots[ipart][0].set_color(p.color)
      if p.color == 'k': self.plots[ipart][0].set_fillstyle('none')
      else:              self.plots[ipart][0].set_fillstyle('full')
      # Set coordinates
      self.plots[ipart][0].set_data(p.x, p.y); 
      values.append(self.plots[ipart][0])        
      ipart+=1
    #self.leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    self.mod = False
    return values

  def draw(self):
    particles = self.universe.GetParticles()
    self.ax.set(xlabel='x', ylabel='y', title='', xlim=(-5,5), ylim=(-5,5))
    self.ax.set_ylim(-self.width, self.width)
    self.ax.set_xlim(-self.height,self.height)
    #text = ax.text(-tam+0.1*tam, tam-0.1*tam,'')#, transform=spl.transAxes)
    self.ax.plot([],[],'ob', label='electron')
    self.ax.plot([],[],'or', label='positron')
    self.ax.plot([],[],'ok', label='photon', fillstyle='none')
    self.leg = self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=3, mode="expand", borderaxespad=0.)

    def init():
      """ Initializing function """
      #text.set_text('')
      values = []
      for j in range(len(universe.GetParticles())):
        self.plots[j][0].set_data([], []); 
        values.append(self.plots[j][0])
      return values

    def reset(event):
      print('Resetting...')
      self.universe.Reset()

    def particleMode(event):
      print('Selecting particle: ', event)
      self.partmode = str(event)
      

    universe = self.universe
    plt.plot([],label='blah')
    anim = ani.FuncAnimation(self.fig,self.update,init_func=init, frames=(100000), interval=100, blit=True)
    print("Drawing...")
    self.button.on_clicked(reset)
    self.particleSelector.on_clicked(particleMode)
    plt.show()
    #if self.savename is not None: anim.save(self.savename+'.mp4', fps=20, dpi=300)
    return anim

