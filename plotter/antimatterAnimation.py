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
from matplotlib.text import Text

axcolor = 'aliceblue'
sliderColor = 'indigo'#'dodgerblue'
textcolor = 'w'
inTextColor = 'k'
bkgcolor = 'k'
electronColor = 'green'
positronColor = 'red'
photonColor = 'w'
borderColor = 'w'

partcolor = {'electron':electronColor, 'positron':positronColor, 'photon':photonColor}

class antimatterAnimation:

  def __init__(self, universe, width=4, savename=None):
    self.fig, self.ax = plt.subplots(facecolor=bkgcolor)
    plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9)
    self.universe = universe
    self.text = ''
    self.plots = []
    self.legplots = []
    self.partmode = 'electron'
    self.savename = savename
    for p in self.universe.GetParticles(): 
      col = partcolor[p.name]
      self.plots.append(self.ax.plot([], [],'o',color = col, fillstyle='none' if p.name=='photon' else 'full'))
    self.width = width
    self.height= self.width
    self.randomSpeedModule = 0.5

    self.ax.set_facecolor(bkgcolor)
    self.ax.spines['bottom'].set_color(borderColor)
    self.ax.spines['top']   .set_color(borderColor)
    self.ax.spines['left']  .set_color(borderColor)
    self.ax.spines['right'] .set_color(borderColor)
    self.ax.xaxis.label.set_color(bkgcolor)
    self.ax.yaxis.label.set_color(bkgcolor)
    self.ax.tick_params(axis='x', colors=bkgcolor)
    self.ax.tick_params(axis='y', colors=bkgcolor)
    
    resetax = plt.axes([0.77, 0.025, 0.14, 0.04])
    for l in ['bottom', 'top', 'left', 'right']: resetax.spines[l].set_color(borderColor)
    self.button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    self.button.label.set_color(inTextColor)

    rmtax    = plt.axes([0.62, 0.025, 0.14, 0.04])
    for l in ['bottom', 'top', 'left', 'right']: rmtax.spines[l].set_color(borderColor)
    self.rmbutton = Button(rmtax, 'Borders OFF', color=axcolor, hovercolor='0.975')
    self.rmbutton.label.set_color(inTextColor)
    
    rax = plt.axes([0.77, 0.075, 0.14, 0.16], facecolor=axcolor)
    for l in ['bottom', 'top', 'left', 'right']: rax.spines[l].set_color(borderColor)
    self.particleSelector = RadioButtons(rax, ('electron', 'positron'), active=0, activecolor=sliderColor)
    #self.particleSelector.label.set_color(inTextColor)

    createax  = plt.axes([0.62, 0.160, 0.14, 0.075], facecolor=axcolor)
    for l in ['bottom', 'top', 'left', 'right']: createax.spines[l].set_color(borderColor)
    self.createRandomPartButtom  = Button(createax, 'Create 25\nparticles', color=axcolor)
    self.createRandomPartButtom.label.set_color(inTextColor)
    createax2 = plt.axes([0.62, 0.075, 0.14, 0.075], facecolor=axcolor)
    for l in ['bottom', 'top', 'left', 'right']: createax2.spines[l].set_color(borderColor)
    self.createRandomPartButtom2 = Button(createax2, 'Create 25\nantiparticles', color=axcolor)
    self.createRandomPartButtom2.label.set_color(inTextColor)

    axmag   = plt.axes([0.20, 0.05, 0.35, 0.03], facecolor=axcolor)
    axelecX = plt.axes([0.20, 0.11, 0.35, 0.03], facecolor=axcolor)
    axelecY = plt.axes([0.20, 0.17, 0.35, 0.03], facecolor=axcolor)
    for l in ['bottom', 'top', 'left', 'right']: axmag.spines[l].set_color(borderColor)
    for l in ['bottom', 'top', 'left', 'right']: axelecX.spines[l].set_color(borderColor)
    for l in ['bottom', 'top', 'left', 'right']: axelecY.spines[l].set_color(borderColor)
    bx,by,bz = self.universe.magneticField.Get()
    ex,ey,ez = self.universe.electricField.Get()
    maxB = self.width/2
    maxE = self.width/2

    self.magFieldSlider   = Slider(axmag,  'Magnetic field', -maxB, maxB, valinit=0, color=sliderColor, valfmt='%1.2f')#bz if abs(bz)<maxB else 0)#, valstep=delta_f)
    self.elecFieldSliderX = Slider(axelecX, 'Electric field (X)', -maxE, maxE, valinit=0, color=sliderColor, valfmt='%1.2f')#ex if abs(ex)<maxE else 0)
    self.elecFieldSliderY = Slider(axelecY, 'Electric field (Y)', -maxE, maxE, valinit=0, color=sliderColor, valfmt='%1.2f')#ey if abs(ey)<maxE else 0)
    self.magFieldSlider.label.set_color(textcolor)
    self.magFieldSlider.valtext.set_color(textcolor)
    self.elecFieldSliderX.label.set_color(textcolor)
    self.elecFieldSliderX.valtext.set_color(textcolor)
    self.elecFieldSliderY.label.set_color(textcolor)
    self.elecFieldSliderY.valtext.set_color(textcolor)

    axrndmspeed = plt.axes([0.93, 0.50, 0.03, 0.15], facecolor=axcolor)
    for l in ['bottom', 'top', 'left', 'right']: axrndmspeed.spines[l].set_color(borderColor)
    self.randomSpeedSlider = Slider(axrndmspeed, 'Particle\nspeed', 0.1, 1, valinit=0.5, orientation='vertical', color=sliderColor)
    self.randomSpeedSlider.label.set_color(textcolor)
    self.randomSpeedSlider.valtext.set_color(textcolor)
    
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
        self.plots.append(self.ax.plot([], [],'o',color = partcolor[p.name], fillstyle=('none' if p.name=='photon' else 'full') ))
      # Set color and style
      self.plots[ipart][0].set_color(partcolor[p.name])
      if p.name == 'photon': self.plots[ipart][0].set_fillstyle('none')
      else:              self.plots[ipart][0].set_fillstyle('full')
      # Set coordinates
      self.plots[ipart][0].set_data(p.x, p.y); 
      values.append(self.plots[ipart][0])        
      ipart+=1
    #self.leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    self.mod = False
    #ipart+=1
    #self.plots.append(self.ax.plot([],[],'ob', label='electron'))
    #values.append(self.plots[ipart][0])
    
    return values

  def draw(self):
    particles = self.universe.GetParticles()
    self.ax.set(xlabel='x', ylabel='y', title='', xlim=(-5,5), ylim=(-5,5))
    self.ax.set_ylim(-self.width, self.width)
    self.ax.set_xlim(-self.height,self.height)
    self.ax.plot([],[],'o', color=electronColor, label='electron')
    self.ax.plot([],[],'o', color=positronColor, label='positron')
    self.ax.plot([],[],'o', color=photonColor, label='photon', fillstyle='none')
    self.leg = self.ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=3, mode="expand", borderaxespad=0., framealpha=0.8, facecolor=bkgcolor, edgecolor=borderColor)
    for t in self.leg.get_texts(): t.set_color(textcolor)
    #self.text1 = self.ax.text(-self.width+2*self.width*0.21, self.height+0.28,'[100]')#, transform=spl.transAxes)

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
      self.magFieldSlider.set_val(0)
      self.elecFieldSliderX.set_val(0)
      self.elecFieldSliderY.set_val(0)

    ##########################################################
    ### Events 

    #on_press event
    def on_press(event):
      mX, mY = self.fig.get_size_inches()*self.fig.dpi
      if event.y < mY*0.291: return
      if event.x > mX*0.8984: return
      print('you pressed', event.button, event.xdata, event.ydata, event.x, event.y)
      if event.xdata == 0 and event.ydata == 0: return
      if event.xdata is None: return
      if abs(event.xdata) > self.width or abs(event.ydata) > self.height: return
      vx = random.uniform(-2,2)*self.randomSpeedModule
      vy = random.uniform(-2,2)*self.randomSpeedModule
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

    def updateRandomSpeed(event):
      print('Moving the random speed to: ', event)
      self.randomSpeedModule = event

    def changeBorders(event):
      print('Moving borders...')
      status = self.universe.doBorders
      label = 'Borders ON' if status else 'Borders OFF'
      self.universe.SetBorders(not status)
      self.rmbutton.label.set_text(label)

    def createRandomPart(event):
      print('Creating random particles...')
      self.universe.CreateRandomParticles(25, 'electron', maxSpeed=self.randomSpeedModule)

    def createRandomPart2(event):
      print('Creating random antiparticles...')
      self.universe.CreateRandomParticles(25, 'positron', maxSpeed=self.randomSpeedModule)

    universe = self.universe
    plt.plot([],label='blah')
    anim = ani.FuncAnimation(self.fig,self.update,init_func=init, frames=(1000), interval=80, blit=True)
    print("Drawing...")

    #### Events
    self.fig.canvas.mpl_connect('button_press_event', on_press)
    self.button.on_clicked(reset)
    self.particleSelector.on_clicked(particleMode)
    self.createRandomPartButtom.on_clicked(createRandomPart)
    self.createRandomPartButtom2.on_clicked(createRandomPart2)
    self.magFieldSlider.on_changed(updateMagField)
    self.elecFieldSliderX.on_changed(updateElecFieldX)
    self.elecFieldSliderY.on_changed(updateElecFieldY)
    self.randomSpeedSlider.on_changed(updateRandomSpeed)
    self.rmbutton.on_clicked(changeBorders)

    plt.show()
    #if self.savename is not None: anim.save(self.savename+'.mp4', fps=20, dpi=300)
    return anim

