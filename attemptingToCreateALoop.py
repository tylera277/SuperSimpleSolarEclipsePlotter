from mpl_toolkits import mplot3d
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sideFunctions import time2Julian, earth2Sun, sun2Moon, vecMathBtwn2Points, rhoPrime
from sideFunctions import leapYearAdjuster
from SolarEclipsePlotter import solarEclipsePlotter
from quickerOverallLoopForChecking import quickApproximateSolarEclipseChecker
from mpl_toolkits.basemap import Basemap
import math
import time


# this gets the position vectors of the stellar bodies that we are using
from jplephem.spk import SPK
kernel = SPK.open('de440.bsp')


yearEclipse = []
possibleSolarEclipseDates = []

# +initial number of days in a month that I set it to, changed according to which month
#
#dayUpperRange = 31

# trying to plot a line from center of sun to center of moon,
# as well as two lines which approximate the diameter of the earth
VecStart_x = [0 for rows in range(20)]
VecEnd_x = [0 for rows in range(20)]
VecStart_y = [0 for rows in range(20)]
VecEnd_y = [0 for rows in range(20)]
VecStart_z = [0 for rows in range(20)]
VecEnd_z = [0 for rows in range(20)]

VecConnection_x = [0 for rows in range(20)]
VecConnection_y = [0 for rows in range(20)]
VecConnection_z = [0 for rows in range(20)]

solarEclipseLat = [[0 for x in range(10000)] for y in range(13)]
solarEclipseLon = [[0 for x in range(10000)] for y in range(13)]
m = 0

# + this is to much more quickly check roughly the month, day, and hour of solar eclipses in a
# specified year range. I will then take these values, use them as bounds for the for loops
# on this page, and use another for loop to get specific minutes. Basically, Im limiting the amount of the year
# that the slower program needs to run through, hopefully speeding the overall program up a little bit.
startYear = 2021
endYear = 2022
data = quickApproximateSolarEclipseChecker(startYear, endYear)
solarMonth = data[0]
solarDay = data[1]
solarHour = data[2]

TestMinute = 0

# +this is how Im going to try to check for possible eclipse dates
#  via this caveman programming for loop, which checks each year,month,day & hour.
# + I have been selecting a specific year in order to compare to resources online to see
#   the accuracy of my model
for TestYear in range(2023, 2024, 1):
    print(TestYear)
    #time.sleep(4)
    for TestMonth in range(10,11,1):
        # this function handles if its a leap year, adjusting the days in that particular month
        dayUpperRange = leapYearAdjuster(TestYear,TestMonth)

        #lower range of this for loop for TestDay was originally 1
        for TestDay in range(1,dayUpperRange,1):
            for TestHour in range(15, 21, 1):
                for TestMinute in range(1,60,10):
                    julianTime = time2Julian(TestYear, TestMonth, TestDay, TestHour,TestMinute)

                    # position of earths center w.r.t. the sun
                    position1 = earth2Sun(julianTime)

                    x1 = position1[0]
                    y1 = position1[1]
                    z1 = position1[2]
                    #print(x1, y1, z1)

# position of moon w.r.t. the sun
                    position2 = sun2Moon(julianTime)

                    x2 = position2[0]
                    y2 = position2[1]
                    z2 = position2[2]
                    #print(x2, y2, z2)


# radius of the respective body (km)
                    r_earth = 6378
                    r_moon = 1737
                    r_sun = 696340

#straight line from center of sun to center of moon
                    VecStart_x[0] = 0
                    VecStart_y[0] = 0
                    VecStart_z[0] = 0
                    VecEnd_x[0] = x2
                    VecEnd_y[0] = y2
                    VecEnd_z[0] = z2

# +line that is perpendicular to the line connecting the sun and the earth,
# parallel with the xy plane (horizontal)
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
# parallel with the xz-plane (vertical)
# +originally centered at the sun but I've translated it by adding x1,y1,z1 to
# it in order to get it centered on the earth
                    vecStart2, vecEnd2 = vecMathBtwn2Points(x2, y2, z2, 1, 0)

                    VecStart_x[2] = vecStart1[0] + x1
                    VecStart_y[2] = vecStart1[1] + y1
                    VecStart_z[2] = (vecStart1[2] + z1) + r_earth
                    VecEnd_x[2] = vecEnd1[0] + x1
                    VecEnd_y[2] = vecEnd1[1] + y1
                    VecEnd_z[2] = (vecEnd1[2] + z1) - r_earth

# + line that is perpendicular to the line connecting the sun and the moon,
# and I have translated it to the moon
# + this is horizontal line(parallel with the xz-plane)
                    vecStart3, vecEnd3 = vecMathBtwn2Points(x2, y2, z2, 1, 0)

                    VecStart_x[3] = (vecStart3[0] + x2) + r_moon
                    VecStart_y[3] = vecStart3[1] + y2
                    VecStart_z[3] = (vecStart3[2] + z2)
                    VecEnd_x[3] = (vecEnd3[0] + x2) - r_moon
                    VecEnd_y[3] = vecEnd3[1] + y2
                    VecEnd_z[3] = (vecEnd3[2] + z2)
# + this is vertical line(parallel with the yz-plane) at the moon
                    vecStart4, vecEnd4 = vecMathBtwn2Points(x2, y2, z2, 1, 0)

                    VecStart_x[4] = (vecStart4[0] + x2)
                    VecStart_y[4] = vecStart4[1] + y2
                    VecStart_z[4] = (vecStart4[2] + z2) + r_moon
                    VecEnd_x[4] = (vecEnd4[0] + x2)
                    VecEnd_y[4] = vecEnd4[1] + y2
                    VecEnd_z[4] = (vecEnd4[2] + z2) - r_moon








                # these are the angle theta from spherical coord.
                # theta plus and minus are angles to get from one side of the earth to the other,horizontally
                # thetaSun2Moon is the angle of the line that goes from sun to moon center

                    thetaPlusEarth = math.atan((VecEnd_y[1]) / (VecEnd_x[1]))
                    thetaMinusEarth = math.atan((VecStart_y[1]) / VecStart_x[1])
                    thetaSun2Moon = math.atan(VecEnd_y[0] / VecEnd_x[0])
                    ####### TEST ########
# lines that are being drawn from center of sun to horizontal edges of the moon
                    thetaSun2Moon1 = math.atan(VecEnd_y[3] / VecEnd_x[3])
                    thetaSun2Moon2 = math.atan(VecStart_y[3] / VecStart_x[3])


                # phi plus and minus are the upper and lower points on the edges of the earth
                # phiSun2Moon is the angle of the line that goes from sun to moon center
                    phiPlusEarth = math.atan((math.sqrt(VecEnd_y[2]**2.0 + VecEnd_x[2]**2.0))/VecEnd_z[2])
                    phiMinusEarth = math.atan((math.sqrt(VecStart_y[2]**2.0 + VecStart_x[2]**2.0))/VecStart_z[2])
                    phiSun2Moon = math.atan((math.sqrt(VecEnd_x[0]**2.0 + VecEnd_y[0]**2.0))/VecEnd_z[0])
# lines that are being drawn from center of sun to vertical edges of the moon
                    phiSun2Moon1 = math.atan((math.sqrt(VecEnd_x[4] ** 2.0 + VecEnd_y[4] ** 2.0)) / VecEnd_z[4])
                    phiSun2Moon2 = math.atan((math.sqrt(VecStart_x[4] ** 2.0 + VecStart_y[4] ** 2.0)) / VecStart_z[4])


                    #print(TestYear,TestMonth,TestDay,TestHour)
                    #print(phiMinusEarth,phiSun2Moon, phiPlusEarth)
                    #print(thetaPlusEarth,thetaSun2Moon, thetaMinusEarth)

# +this checks whether the angle of the line from the sun's center to the moons
# center is within the range of the angle from left/right
# and top/bottom parts of the earth. Im using 2 lines to approximate the cross
# section of the earth right now, may update that later for better accuracy.

# + The last check of this if statement I had to switch the bounds for theta in order for it to get
# solar and lunar eclipses later in the year, not entirely sure why though
                    #if ((phiMinusEarth <= phiSun2Moon <= phiPlusEarth) and
                    #    (thetaPlusEarth <= thetaSun2Moon <= thetaMinusEarth)) or \
                    #    ((phiMinusEarth <= phiSun2Moon <= phiPlusEarth) and
                    #     (thetaMinusEarth <= thetaSun2Moon <= thetaPlusEarth)):

                    if ((0.9995*phiMinusEarth <= phiSun2Moon1 <= 1.0005*phiPlusEarth) or (0.9995*phiMinusEarth <= phiSun2Moon2 <= 1.0005*phiPlusEarth)) and \
                            (((0.9995*thetaPlusEarth <= thetaSun2Moon1 <= 1.0005*thetaMinusEarth) or (0.9995*thetaPlusEarth <= thetaSun2Moon2 <= 1.0005*thetaMinusEarth)) or \
                             (0.9995*thetaMinusEarth <= thetaSun2Moon1 <= 1.0005*thetaPlusEarth) or (0.9995*thetaMinusEarth <= thetaSun2Moon2 <= 1.0005*thetaPlusEarth)) :

                        possibleSolarEclipseDates.append(julianTime)
                        #yearEclipse.append(TestYear)
                        #print('#########################')
                        #print(phiMinusEarth, phiSun2Moon, phiPlusEarth)
                        #print(thetaPlusEarth, thetaSun2Moon, thetaMinusEarth)
                        #print(TestYear,TestMonth,TestDay,TestHour)
                        #print(possibleSolarEclipseDates)


# +trying to start to work on plotting the course of the solar eclipse onto the earth.
                        # +this detects if its a solar eclipse, as that is all that can be plotted on earth
                        if np.sqrt(x1**2+y1**2+z1**2) > np.sqrt(x2**2+y2**2+z2**2):
                            print(TestYear, TestMonth, TestDay, TestHour, TestMinute)
                            print(solarEclipsePlotter(TestYear, TestMonth, TestDay, TestHour, TestMinute))

                        if solarEclipsePlotter(TestYear, TestMonth, TestDay, TestHour, TestMinute) != (0,0):
                            solarEclipseLat[TestMonth][m] = (solarEclipsePlotter(TestYear, TestMonth, TestDay, TestHour, TestMinute))[0]
                            solarEclipseLon[TestMonth][m] = (solarEclipsePlotter(TestYear, TestMonth, TestDay, TestHour, TestMinute))[1]
                            m += 1

for l in range(13):
    for h in range(len(solarEclipseLat)):

        print("arrr:",l,h,":", solarEclipseLat[l][h])

# + below this is concerned with the plotting of the points onto a world map

m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, \
            llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral', lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90., 91., 30.))
m.drawmeridians(np.arange(-180., 181., 60.))
m.drawmapboundary(fill_color='aqua')
plt.title("Mercator Projection")

# +I'm not sure how to plot the points in relation to each event, like the lat&lon generated for one solar eclipse
# not plotting in different ones. How to display the coordinates of each solar eclipse event, one event at a time

lon1 = solarEclipseLon[10]
lat1 = solarEclipseLat[10]
x1,y1 = m(lon1, lat1)
m.plot(x1, y1, 'bo', markersize=3)


plt.show()