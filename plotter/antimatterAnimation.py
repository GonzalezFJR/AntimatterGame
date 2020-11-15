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
    
    resetax = plt.axes([0.77, 0.025, 0.14, 0.04])
    self.button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    
    rax = plt.axes([0.77, 0.068, 0.14, 0.15], facecolor=axcolor)
    self.particleSelector = RadioButtons(rax, ('electron', 'positron'), active=0)

    axmag   = plt.axes([0.20, 0.08, 0.45, 0.03], facecolor=axcolor)
    axelecX = plt.axes([0.20, 0.14, 0.45, 0.03], facecolor=axcolor)
    axelecY = plt.axes([0.20, 0.20, 0.45, 0.03], facecolor=axcolor)
    bx,by,bz = self.universe.magneticField.Get()
    ex,ey,ez = self.universe.electricField.Get()
    maxB = self.width/2
    maxE = self.width/2

    self.magFieldSlider   = Slider(axmag,  'Magnetic field', -maxB, maxB, valinit=bz if abs(bz)<maxB else 0)#, valstep=delta_f)
    self.elecFieldSliderX = Slider(axelecX, 'Electric field (X)', -maxE, maxE, valinit=ex if abs(ex)<maxE else 0)
    self.elecFieldSliderY = Slider(axelecY, 'Electric field (Y)', -maxE, maxE, valinit=ey if abs(ey)<maxE else 0)
    
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
      self.universe.SetMagneticField(0)
      self.universe.SetElectricField(0,0)

    ##########################################################
    ### Events 

    #on_press event
    def on_press(event):
      if event.y < 140: return
      print('you pressed', event.button, event.xdata, event.ydata)
      if event.xdata == 0 and event.ydata == 0: return
      if event.xdata is None: return
      vx = random.uniform(-1,1)
      vy = random.uniform(-1,1)
      if abs(event.xdata) > self.width or abs(event.ydata) > self.height: return
      self.universe.AddParticle(NewParticle(self.partmode, event.xdata, event.ydata, vx, vy))
      self.mod = True

    def particleMode(event):
      print('Selecting particle: ', event)
      self.partmode = str(event)
      
    def updateMagField(event):
      print('Moving magnetic filed to: ', event)
      self.universe.SetMagneticField(event)

    def updateElecFieldX(event):
      print('Moving electric filed X to: ', event)
      self.universe.SetElectricField(x=event)

    def updateElecFieldY(event):
      print('Moving electric filed Y to: ', event)
      self.universe.SetElectricField(y=event)

    universe = self.universe
    plt.plot([],label='blah')
    anim = ani.FuncAnimation(self.fig,self.update,init_func=init, frames=(1000), interval=80, blit=True)
    print("Drawing...")

    #### Events
    self.fig.canvas.mpl_connect('button_press_event', on_press)
    self.button.on_clicked(reset)
    self.particleSelector.on_clicked(particleMode)
    self.magFieldSlider.on_changed(updateMagField)
    self.elecFieldSliderX.on_changed(updateElecFieldX)
    self.elecFieldSliderY.on_changed(updateElecFieldY)

    plt.show()
    #if self.savename is not None: anim.save(self.savename+'.mp4', fps=20, dpi=300)
    return anim

