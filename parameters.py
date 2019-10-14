# dynamic model
L = 100 # arena size
N = 50 # number of boids
R = 5 # interaction radius
dT = 0.1 # for numeric integration

# display
W = 1000
H = int(W*2/3)
BOIDSIZE = L/20

# utils
UGRIDLENGTH = int(L / R)
UGRIDCELLSIZE = L / UGRIDLENGTH
