import datetime
import math

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
    moon2SunCenter = kernel[0, 3].compute(julianTime) # this is sun to earth's barycenter
    moon2SunCenter += kernel[3, 301].compute(julianTime) # from earths barycenter to moon's center

    return moon2SunCenter


def leapYearAdjuster(year, month):
    if year % 4 == 0 and year % 400 == 0 and year % 100 != 0 and month == 2:
        dayUpperRange = 28
    elif month ==2:
        dayUpperRange = 29
    elif month == 9 or 4 or 6 or 11:
        dayUpperRange = 30

    return dayUpperRange



