from mpl_toolkits import mplot3d
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sideFunctions import time2Julian, earth2Sun, sun2Moon, vecMathBtwn2Points
import math

# this creates the raw blank figure
fig = plt.figure()
#ax = plt.axes(projection='3d')
ax = fig.add_subplot(projection='3d')
#ax.set_xlim(-1.5*10**8,1.5*10**8)
#ax.set_ylim(-1.5*10**8, 1.5*10**8)
#ax.set_zlim(-1.5*10**8, 1.5*10**8)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# this gets the position vectors of the stellar bodies that we are using
from jplephem.spk import SPK
kernel = SPK.open('de440.bsp')

year = 2021
month = 5
day = 1
hour = 0

julianTime = time2Julian(year, month, day, hour)
print(julianTime)
# position of earths center w.r.t. the sun
#position1 = earth2Sun(julianTime)

# +this is to test when I want to check if the circle that i have placed representing
# the earths cross section is still there, at its normal distance, the cirle becomes too
# small to be able to see
###### T E S T ########
position1 = [0,0,0]
###### T E S T ######
x1 = position1[0]
y1 = position1[1]
z1 = position1[2]*math.cos(math.degrees(23.5))
print(x1, y1, z1)

# position of moon w.r.t. the sun
position2 = sun2Moon(julianTime)
##### T E S T ########
#position2 = kernel[3,399].compute(julianTime)
#position2 += kernel[3,301].compute(julianTime)
##### T E S T ########

x2 = position2[0]
y2 = position2[1]
z2 = position2[2] *math.cos(math.degrees(23.5)) # +I added this cosine term b/c for some reason JPL ephemeris gives
print(x2, y2, z2)                               #  out the coordinates with respect to earth's tilt,
                                                # so I think I got rid of that  with the cos term


# radius of the respective body (km)
r_earth = 6378
r_moon = 1737
r_sun = 696340

# the dots representing each planetary body
ax.scatter(x1, y1, z1, s=r_earth/1000, c='green')
#ax.scatter(x2, y2, z2, s=r_moon/1000, c='gray')
#ax.scatter(0, 0, 0, s=r_sun/1000, c='yellow')

# trying to plot a line from center of sun to center of moon
VecStart_x = [0 for rows in range(3)]
VecEnd_x = [0 for rows in range(3)]
VecStart_y = [0 for rows in range(3)]
VecEnd_y = [0 for rows in range(3)]
VecStart_z = [0 for rows in range(3)]
VecEnd_z = [0 for rows in range(3)]



#straight line from center of sun to center of moon
#VecStart_x[0] = 0
#VecStart_y[0] = 0
#VecStart_z[0] = 0
#VecEnd_x[0] = x2
#VecEnd_y[0] = y2
#VecEnd_z[0] = z2

# +line that is perpendicular to the line connecting the sun and the earth,
# horizontal with the xy-plane
# originally centered at the sun but I've translated it by adding x1,y1,z1 to
# it in order to get it centered on the earth
vecStart1, vecEnd1 = vecMathBtwn2Points(x2, y2, z2, 1, 0)

VecStart_x[1] = (vecStart1[0] + x1)+r_earth
VecStart_y[1] = vecStart1[1] + y1
VecStart_z[1] = vecStart1[2] + z1
VecEnd_x[1] = (vecEnd1[0] + x1)-r_earth
VecEnd_y[1] = vecEnd1[1] + y1
VecEnd_z[1] = vecEnd1[2] + z1

# +line that is perpendicular to the line connecting the sun and the earth,
#  horizontal with the xz-plane
vecStart2, vecEnd2 = vecMathBtwn2Points(x2, y2, z2, 1, 0)

VecStart_x[2] = vecStart1[0] + x1
VecStart_y[2] = vecStart1[1] + y1
VecStart_z[2] = (vecStart1[2] + z1) + r_earth
VecEnd_x[2] = vecEnd1[0] + x1
VecEnd_y[2] = vecEnd1[1] + y1
VecEnd_z[2] = (vecEnd1[2] + z1) - r_earth



# this puts a circle that faces the sun on earth, representing the middle cross section
theta = np.linspace(0, 2 * np.pi, 201)
x = np.cos(theta)*r_earth +x1
z = np.sin(theta)*r_earth +z1
y = np.zeros(201) +y1
ax.plot(x,y,z,c='red')

# trying to tell whether the line from sun to middle of sun hits the earths cross section

for i in range(3):
    ax.plot([VecStart_x[i], VecEnd_x[i]], [VecStart_y[i],VecEnd_y[i]],[VecStart_z[i],VecEnd_z[i]])

plt.show()