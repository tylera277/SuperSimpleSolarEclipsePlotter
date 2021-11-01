from mpl_toolkits import mplot3d
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sideFunctions import time2Julian, earth2Sun, sun2Moon
from sideFunctions import leapYearAdjuster
from eclipsePlotter import EclipsePlotter

import math
import time
from angleCalculations import AngleCalculations as angleCalc


# this gets the position vectors of the stellar bodies that we are using
from jplephem.spk import SPK
kernel = SPK.open('de440.bsp')


yearEclipse = []
possibleSolarEclipseDates = np.zeros((13, 1000))


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

m = 0


# + These for loops check each date to see whether it meets the criteria below,
#   basically that the moons shadow hits somewhere within the cross section of the earth.
# + I have been selecting a specific year in order to compare to resources online to see
#   the accuracy of my model.
for TestYear in range(2023, 2024, 1):

    for TestMonth in range(10, 11, 1):
        counter = 0
        print(TestMonth)
        # this function handles if its a leap year, adjusting the days in that particular month
        dayUpperRange = leapYearAdjuster(TestYear, TestMonth)

        for TestDay in range(1, dayUpperRange, 1):
            for TestHour in range(1, 24, 1):
                for TestMinute in range(1, 60, 1):


                    # This gets the julian date for that specific time of year
                    julianTime = time2Julian(TestYear, TestMonth, TestDay, TestHour, TestMinute)

                    # position of earths center w.r.t. the sun
                    position1 = earth2Sun(julianTime)

                    xEarthCent = position1[0]
                    yEarthCent = position1[1]
                    zEarthCent = position1[2]

                    # position of moon w.r.t. the sun
                    position2 = sun2Moon(julianTime)

                    xMoonCent = position2[0]
                    yMoonCent = position2[1]
                    zMoonCent = position2[2]

                    # radius of the respective body (km)
                    r_earth = 6378
                    r_moon = 1737

                    # straight line from center of sun to center of moon
                    VecStart_x[0] = 0
                    VecStart_y[0] = 0
                    VecStart_z[0] = 0
                    VecEnd_x[0] = xMoonCent
                    VecEnd_y[0] = yMoonCent
                    VecEnd_z[0] = zMoonCent

                    # +line that is perpendicular to the line connecting the sun and the earth,
                    # parallel with the xy plane (horizontal)
                    # originally centered at the sun but I've translated it by adding x1,y1,z1 to
                    # it in order to get it centered on the earth

                    VecStart_x[1] = xEarthCent+r_earth
                    VecStart_y[1] = yEarthCent
                    VecStart_z[1] = zEarthCent
                    VecEnd_x[1] = xEarthCent - r_earth
                    VecEnd_y[1] = yEarthCent
                    VecEnd_z[1] = zEarthCent

                    # +line that is perpendicular to the line connecting the sun and the earth,
                    # parallel with the xz-plane (vertical)
                    # +originally centered at the sun but I've translated it by adding x1,y1,z1 to
                    # it in order to get it centered on the earth

                    VecStart_x[2] = xEarthCent
                    VecStart_y[2] = yEarthCent
                    VecStart_z[2] = zEarthCent + r_earth
                    VecEnd_x[2] = xEarthCent
                    VecEnd_y[2] = yEarthCent
                    VecEnd_z[2] = zEarthCent - r_earth

                    # + line that is perpendicular to the line connecting the sun and the moon,
                    # and I have translated it to the moon
                    # + this is horizontal line(parallel with the xz-plane)

                    VecStart_x[3] = xMoonCent + r_moon
                    VecStart_y[3] = yMoonCent
                    VecStart_z[3] = zMoonCent
                    VecEnd_x[3] = xMoonCent - r_moon
                    VecEnd_y[3] = yMoonCent
                    VecEnd_z[3] = zMoonCent

                    # + this is vertical line(parallel with the yz-plane) at the moon
                    vecStart4, vecEnd4 = [0, 0, 0], [0, 0, 0]

                    VecStart_x[4] = xMoonCent
                    VecStart_y[4] = yMoonCent
                    VecStart_z[4] = zMoonCent + r_moon
                    VecEnd_x[4] = xMoonCent
                    VecEnd_y[4] = yMoonCent
                    VecEnd_z[4] = zMoonCent - r_moon


                # these are the angle theta from spherical coord.
                # theta plus and minus are angles to get from one side of the earth to the other,horizontally
                    thetaPlusEarth = angleCalc(VecEnd_x[1], VecEnd_y[1], VecEnd_z[1]).theta()
                    thetaMinusEarth = angleCalc(VecStart_x[1], VecStart_y[1], VecStart_z[1]).theta()
                # lines that are being drawn from center of sun to horizontal edges of the moon
                    thetaSun2Moon1 = angleCalc(VecEnd_x[3], VecEnd_y[3], VecEnd_z[3]).theta()
                    thetaSun2Moon2 = angleCalc(VecStart_x[3], VecStart_y[3], VecStart_z[3]).theta()



                # phi plus and minus are the upper and lower points on the edges of the earth
                    phiPlusEarth = angleCalc(VecEnd_x[2], VecEnd_y[2], VecEnd_z[2]).phi()
                    phiMinusEarth = angleCalc(VecStart_x[2], VecStart_y[2], VecStart_z[2]).phi()
                # lines that are being drawn from center of sun to vertical edges of the moon
                    phiSun2Moon1 = angleCalc(VecEnd_x[4], VecEnd_y[4], VecEnd_z[4]).phi()
                    phiSun2Moon2 = angleCalc(VecStart_x[4], VecStart_y[4], VecStart_z[4]).phi()



                    # +this checks whether the angle of the line from the sun's center to the moons horizontal
                    # and vertical edges, where I have split the moon's cross section into two perpendicular lines,
                    # is within the range of the angle from left/right
                    # and top/bottom parts of the earth, same thing being done to the earth as was done to the moon.



                    if ((phiMinusEarth <= phiSun2Moon1 <= phiPlusEarth) or (phiMinusEarth <= phiSun2Moon2 <= phiPlusEarth)) and \
                            (((thetaPlusEarth <= thetaSun2Moon1 <= thetaMinusEarth) or (thetaPlusEarth <= thetaSun2Moon2 <= thetaMinusEarth)) or \
                             ((thetaMinusEarth <= thetaSun2Moon1 <= thetaPlusEarth) or (thetaMinusEarth <= thetaSun2Moon2 <= thetaPlusEarth))):

                        print(TestYear, TestMonth, TestDay, TestHour, TestMinute)

                        # this filters out the solar from the lunar eclipses
                        if (((xMoonCent**2+yMoonCent**2+zMoonCent)**(1/2)) < ((xEarthCent**2+yEarthCent**2+zEarthCent)**(1/2))):
                            possibleSolarEclipseDates[TestMonth][counter] = (julianTime)
                            counter += 1

lat, lon = EclipsePlotter(possibleSolarEclipseDates).latANDlonFinder()
blurb = EclipsePlotter(possibleSolarEclipseDates).plotter(lat, lon)


