from mpl_toolkits import mplot3d
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sideFunctions import time2Julian, earth2Sun, sun2Moon, vecMathBtwn2Points, rhoPrime
from sideFunctions import leapYearAdjuster

import math
import time
from angleCalculations import AngleCalculations as angleCalc


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
#startYear = 2021
#endYear = 2022
#data = quickApproximateSolarEclipseChecker(startYear, endYear)
#solarMonth = data[0]
#solarDay = data[1]
#solarHour = data[2]

TestMinute = 0

# +this is how Im going to try to check for possible eclipse dates
#  via this caveman programming for loop, which checks each year,month,day & hour.
# + I have been selecting a specific year in order to compare to resources online to see
#   the accuracy of my model
for TestYear in range(2021, 2022, 1):
    print(TestYear)
    #time.sleep(4)
    for TestMonth in range(1,12,1):
        # this function handles if its a leap year, adjusting the days in that particular month
        dayUpperRange = leapYearAdjuster(TestYear,TestMonth)

        #lower range of this for loop for TestDay was originally 1
        for TestDay in range(1,dayUpperRange,1):
            for TestHour in range(1, 24, 1):
                for TestMinute in range(1,60,60):
                    julianTime = time2Julian(TestYear, TestMonth, TestDay, TestHour,TestMinute)

