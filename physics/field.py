"""
  A few classes to create and store values for magnetic and electric fields and their representation
"""

class fieldType:
  none     = 0
  magnetic = 1
  electric = 2

class field:
  def __init__(self, x=0, y=0, z=0, fieldType=fieldType.none):
    """ For the moment, the fiel is costant. The vector (x,y) defines the field """
    self.x = x
    self.y = y
    self.z = z
    self.SetType(fieldType)

  def SetType(self, t=fieldType.none):
    self.type = t

  def SetField(self, x, y, z=0):
    self.x = x
    self.y = y
    self.z = z

  def SetHorizontalUp(self, mag=1):
    self.x = mag
    self.y = 0
    self.z = 0

  def SetHorizontalDown(self, mag=1):
    self.x = -mag
    self.y = 0
    self.z = 0

  def SetVerticalUp(self, mag=1):
    self.x = 0
    self.y = mag
    self.z = 0

  def SetVerticalDown(self, mag=1):
    self.x = 0
    self.y = -mag
    self.z = 0

  def SetInward(self, mag=1):
    self.x = 0
    self.y = 0
    self.z = -mag

  def SetOutward(self, mag):
    self.x = 0
    self.y = 0
    self.z = 0

  def SetZfield(self, mag):
    self.x = 0
    self.y = 0
    self.z = mag

  def SetVertical(self, mag=1):
    if mag>0: self.SetVerticalUp(mag)
    else    : self.SetVerticalDown(mag)

  def SetHorizontal(self, mag=1):
    if mag>0: self.SetHorizontalUp(mag)
    else    : self.SetHorizontalDown(mag)

  def GetValue(self):
    return [x,y]

  def IsMagnetic(self):
    return self.type == fieldType.magnetic

  def IsElectic(self):
    return self.type == fieldType.electric

  def GetType(self):
    return self.type

  def Get(self):
    return [self.x, self.y, self.z]

  ### Drawing options
  #############################################
  #
  # Todo: How should we draw a field????
  #
  def SetColor(self, color):
    self.color = color

  def SetAlpha(self, alpha=1):
    self.alpha = 1

  def SetColorAlpha(self, color, alpha=1):
    self.SetColor(color)
    self.SetAlpha(alpha)

  def SetStyle(self, style):
    """ Just in case we implement several styles... maybe arrows or filled color, large arrows... """
    self.style = style


class magneticField(field):
  """ A field with magnetic type """ 

  def __init__(self, z=0, x=0, y=0):
    self.x = x
    self.y = y
    self.z = z
    self.SetType(fieldType.magnetic)

  def SetType(self, t=None):
    return


class electricField(field):
  """ A field with electric type """

  def __init__(self, x=0, y=0, z=0):
    self.x = x
    self.y = y
    self.z = z
    self.SetType(fieldType.electric)

  def SetType(self, t=None):
    return



