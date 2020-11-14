import numpy as np
from numpy.linalg import inv

def GetOmegaMatrix(B, dt, charge, mass):
  bx, by, bz = B
  matrix = np.array([ [0, -bz, by], [bz, 0, bx], [-by, -bx, 0] ])*(charge/mass*dt)
  return matrix

def GetInvertedOmegaPlusI(omega):
  I = np.eye(3)
  X = I+omega
  return inv(X) 

def GetRmatrix(omega):
  I = np.eye(3)
  X = GetInvertedOmegaPlusI(omega)
  return np.dot(X, (I-omega))

def GetNextWithBoris(dt, x, v, B, E, mass=1, charge=1, c=1):
  q,m = charge, mass
  omega = GetOmegaMatrix(B, dt, q, m)
  I = np.eye(3)
  X = GetInvertedOmegaPlusI(omega)
  R = GetRmatrix(omega)
  if isinstance(E, list): E = np.array(E)
  x = x + np.dot(R, v)*dt + (q/m*dt*dt)*np.dot(X, E)
  v = np.dot(R,v) + (q/m*dt)*np.dot(X, E)
  return x, v

