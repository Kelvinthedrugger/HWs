# AUTOGENERATED! DO NOT EDIT! File to edit: oval_clean.ipynb (unless otherwise specified).

__all__ = ['cov', 'numpts', 'Points', 'vlen', 'major', 'minor', 'x_vec', 'dot', 'ang', 'rat', 'major_length',
           'minor_length', 'transform_x', 'transform_y', 'cos', 'sin', 'theta', 'x', 'y', 'x_oval', 'y_oval',
           'Points_map', 'boundary', 'xx', 'y1', 'y2']

# Cell
import numpy as np
from matplotlib import pyplot as plt

# Cell
# the cov matrix
# sig1 = 2, sig2 = 1, rho = 0.5
cov = [[4,1],[1,1]]

# Cell
# get the points first makes more sense
numpts = 3000
Points = np.random.multivariate_normal([0,0],cov,size=numpts)

# Cell
# get vector length
def vlen(v):
    return np.sqrt( np.square(v[-2]) + np.square(v[-1]))

# try it
vlen(np.array([1,2])), vlen(np.array([3,4]))

# Cell
# get the eigvals and vecs
eigvals, eigvecs = np.linalg.eig(np.array(cov))
eigvals, eigvecs

# Cell
major = eigvecs.T[0]
major

# Cell
minor = eigvecs.T[1]
minor

# Cell
# find the angle of major axis to x axis
# take advantage of high school math: dot product
x_vec = np.array([1,0])
dot = major @ x_vec
ang = np.arccos(dot/(vlen(major)*vlen(x_vec)))
ang * 180 / np.pi

# Cell
""" 0.59 meets but i don't know why """ # gets 0.502
rat = 0.59 # 1/sqrt(5) times of standard deviation !?
major_length = 2*eigvals[0]**0.5 * rat
minor_length = 2*eigvals[1]**0.5 * rat
major_length, minor_length

# Cell
# get the ellipse again use high school math
cos = np.cos(ang)
sin = np.sin(ang)

def transform_x(x,y):
    return x*cos + y*sin

def transform_y(x,y):
    return x*sin - y*cos

theta = np.arange(0,360,1)*np.pi/180
x = major_length*np.cos(theta)
y = minor_length*np.sin(theta)

x_oval = transform_x(x,y)
y_oval = transform_y(x,y)

# Cell
# define boundary and calculate inside/total
Points_map = [[transform_x(ele[0],ele[1]),transform_y(ele[0],ele[1])] for ele in Points]

# Cell
def boundary(point):
    return vlen([point[0]*minor_length,point[1]*major_length])

# Cell
# check if the point is inside the boundary
pts, pts2 = [], []
for i in range(numpts):
    if boundary(Points_map[i]) < major_length*minor_length:
        pts.append(Points[i])
    else:
        pts2.append(Points[i])

# Cell
ptsn, ptsn2 = np.array(pts), np.array(pts2)

# Cell
# major and minor axis line
xx = np.arange(-8,8,1/numpts)
y1 = xx * major[1]/major[0]
y2 = xx * minor[1]/minor[0]

# Cell
# result
plt.figure(figsize=(9,9))
plt.plot(x_oval,y_oval,"purple",linewidth=5.0)
plt.scatter(ptsn[:,0],ptsn[:,1])
plt.scatter(ptsn2[:,0],ptsn2[:,1])
plt.plot(xx,y1,"black")
plt.plot(xx,y2,"green")

plt.xlim([-4,4])
plt.ylim([-4,4])
plt.legend(["contour","major","minor","inside","outside"])
plt.title(chr(ord('%')) + "std: %.4f; inside/total: %.4f" % (rat, len(ptsn)/numpts))
# change the filename each time, can use os.scandir() to write the right filename automatically
import os
if not os.path.isfile("multnormal\output.png"):
    plt.savefig('output')
plt.show()