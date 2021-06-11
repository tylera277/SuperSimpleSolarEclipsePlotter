import ephem

year1 = 2023
month1 = 10
day1 = 14
hour1 = 17

sun, moon = ephem.Sun(), ephem.Moon()
testDate = "{}/{}/{} {}:00:00 ".format(year1, month1, day1, hour1)

test = ephem.Observer()
test.date = testDate

#for i in range(-90,90,1):
#    for j in range(-180,179,1):
i = 0
j = 0

test.lon, test.lat = "{}".format(i), '{}'.format(j)
sun.compute(test)
moon.compute(test)

#print(sun.ra,moon.ra)
#print(moon.ra, moon.dec)
#print(float(sun.ra), float(moon.ra))
#print(float(sun.dec), float(moon.dec))

#print(13 + float(13)/60 + float(14.90/3600))
#print(13 + float(17)/60 + float(55.68)/3600)
x = str(sun.ra)
y = x.split(":")
#print(float(y[0]) + float(y[1])/60 + float(y[2])/3600)

l = str(moon.ra)
m = l.split(":")
o = float(y[0]) + float(y[1])/60 + float(y[2])/3600
#print(float(m[0]) + float(m[1])/60 + float(m[2])/3600)

def DMStoDD(string):
    a = str(string)
    b = a.split(":")
    c = float(b[0]) + float(b[1])/60 + float(b[2])/3600
    return c

n = DMStoDD(sun.ra)
print(n)