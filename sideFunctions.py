import datetime
import math

# code from https://www.geeksforgeeks.org/python-pandas-timestamp-to_julian_date/

import pandas as pd
from jplephem.spk import SPK

def time2Julian(year1, month1, day1, hour1, minute1):

    # Create the Timestamp object
    ts = pd.Timestamp(year=year1, month=month1, day=day1,
                  hour=hour1, minute=minute1, second=00, tz='US/Eastern')

    # Print the Timestamp object
    return ts.to_julian_date()

# returns the position of the center of the earth to the center of the sun
def earth2Sun(julianTime):
    kernel = SPK.open('de440.bsp')
    sun2EarthCenter = kernel[0, 3].compute(julianTime) # this is sun to earth's barycenter
    sun2EarthCenter += kernel[3, 399].compute(julianTime) # moves from earths barycenter to center

    return sun2EarthCenter

# returns the position of the moon to the center of the sun
def sun2Moon(julianTime):
    kernel = SPK.open('de440.bsp')
    moon2SunCenter = kernel[0,3].compute(julianTime) # this is sun to earth's barycenter
    moon2SunCenter += kernel[3,301].compute(julianTime) # from earths barycenter to moon's center

    return moon2SunCenter

# +
# +the refPoint is used in calculating a line that is perpendicular to the line connecting the
# two bodies. Im planning on just using x=+/-1,y=0,z=+/-(x1*x-y1*y)/(-z1) for all of my calculations.
# Interchange x1 and x2 for whichever body you're calculating for
def vecMathBtwn2Points(x1,y1,z1,refPointx,refPointy):
    VecStart = [0 for rows in range(3)]
    VecEnd = [0 for rows in range(3)]



   # refPointx = refpointx # set to 1
   # refPointy = refpointy# set to 0

    VecStart[0] = +refPointx
    VecStart[1] = refPointy
    VecStart[2] = -((x1*refPointx)+y1*refPointy)/z1
    VecEnd[0] = -refPointx
    VecEnd[1] = refPointy
    VecEnd[2] = -((x1*-refPointx)+(y1*refPointy))/z1

    return VecStart,VecEnd

def leapYearAdjuster(year,month):
    if year % 4 == 0 and year % 400 == 0 and year % 100 != 0 and month == 2:
        dayUpperRange = 28
    elif month ==2:
        dayUpperRange = 29
    elif month == 9 or 4 or 6 or 11:
        dayUpperRange = 30

    return dayUpperRange

def rhoPrime(theta,phi,deltaX,deltaY,deltaZ,radius):

    a = ((math.sin(phi))**2 * (math.cos(theta))**2) + ((math.sin(phi))**2 + (math.sin(theta))**2) + (math.cos(phi))**2
    b = (2 * deltaX * math.sin(phi) * math.cos(theta)) + (2 * deltaY * math.sin(phi) * math.sin(theta)) + (2 * deltaZ*math.cos(phi))
    c = deltaX**2 + deltaY**2 + deltaZ**2 - radius**2
    print(a, b**2, c)

    rho_prime = (-b + math.sqrt(b**2 - 4 * a * c))/(2 * a)

    return rho_prime


