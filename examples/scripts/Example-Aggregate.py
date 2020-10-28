import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
sys.path.append('/cds/home/i/iris/pysingfel')
import pysingfel as ps
from pysingfel.particlePlacement import *

def drawSphere(xCenter, yCenter, zCenter, r):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    x = r*x + xCenter
    y = r*y + yCenter
    z = r*z + zCenter
    return (x,y,z)

input_dir='../input'
beamfile=input_dir+'/beam/amo86615.beam'
geom=input_dir+'/lcls/amo86615/PNCCD::CalibV1/Camp.0:pnCCD.1/geometry/0-end.data'
pdbfile=input_dir+'/pdb/3iyf.pdb'

beam = ps.Beam(beamfile)
beam.photon_energy = 1600.0 # reset the photon energy
print ("photon energy=", beam.photon_energy)
print ("beam radius=", beam._focus_xFWHM/2)
print ("focus area=", beam._focus_area)
print ("number of photons per shot=", beam._n_phot)

det = ps.PnccdDetector(geom=geom, beam=beam)
det.distance = 0.581*0.5
print ("detector distance=", det.distance)

particle = ps.Particle()
particle.read_pdb(pdbfile, ff='WK')

num = 8
experiment = ps.FXSExperiment(det=det, beam=beam, jet_radius=1e-4, particles=[particle], n_part_per_shot=num, gamma=1.)
particle_group = experiment.generate_new_sample_state()
part_positions = particle_group[0][0]
radius = max_radius({particle: num})

x = []
y = []
z = []
for i in range(num):
    x.append(part_positions[i,0])
    y.append(part_positions[i,1])
    z.append(part_positions[i,2])
x = np.array(x)
y = np.array(y)
z = np.array(z)
r = np.ones(num)*radius

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
for (xi,yi,zi,ri) in zip(x,y,z,r):
    (xs,ys,zs) = drawSphere(xi,yi,zi,ri)
    ax.plot_wireframe(xs, ys, zs)
    plt.locator_params(axis='x', nbins=3)
    plt.locator_params(axis='y', nbins=3)
    plt.locator_params(axis='z', nbins=3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
plt.show()
