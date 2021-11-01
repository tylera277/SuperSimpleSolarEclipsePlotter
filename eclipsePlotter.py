
class EclipsePlotter:

    def __init__(self, solarEclipseDates):
        self.solarEclipseDates = solarEclipseDates


    def latANDlonFinder(self):
        """
        Function which finds the latitude and longitude on Earth, at the times of the solar eclipses
        that I have predicted, where the altitude and azimuth of the sun and moon are nearly exactly the
        same, within a very small margin.
        """
        import ephem
        import pandas as pd
        import matplotlib.pyplot as plt

        solarEclipseLat = []
        solarEclipseLon = []




        for i in range(len(self.solarEclipseDates[10])):


            if (self.solarEclipseDates[10][i] == 0):

                break

            moon = ephem.Moon()
            sun = ephem.Sun()
            obsPosition = ephem.Observer()
            time = pd.to_datetime(self.solarEclipseDates[10][i], unit='D', origin='julian')


            for lat1 in range(-90, 90, 1):
                for lon1 in range(-180, 180, 1):




                    obsPosition.lat = "{}".format(lat1)
                    obsPosition.long = "{}".format(lon1)
                    obsPosition.date = "{}".format(time)

                    sun.compute(obsPosition)
                    moon.compute(obsPosition)

                    moonAz = moon.az + 0.0
                    moonAlt = moon.alt + 0.0

                    sunAz = sun.az + 0.0
                    sunAlt = sun.alt + 0.0

                    if ((abs(sunAlt - moonAlt) < 0.0001) and ((abs(sunAz - moonAz) < 0.0001))):
                        solarEclipseLat.append(lat1)
                        solarEclipseLon.append(lon1)

                        # print(abs(sunAlt - moonAlt))
                        # print(abs(sunAz - moonAz))

        #print(solarEclipseLon)
        #print(solarEclipseLat)

        return solarEclipseLat, solarEclipseLon

    def plotter(self, lat, lon):
        """
        Function which plots the points of latitude and longitude from the
        function above onto a map.
        """

        import numpy as np
        import plotly.express as px
        import matplotlib.pyplot as plt
        import pandas as pd


        df = pd.DataFrame(lat)
        df.columns = ['lat']
        df['lon'] = lon


        fig = px.scatter_geo(df, lat='lat', lon='lon')
        fig.update_layout(title='5/29/1919 Solar Eclipse Path', title_x=0.5)
        fig.show()
