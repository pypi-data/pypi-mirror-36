"""Region Class
"""
from energy_demand.geography import weather_station_location

class Region(object):
    """Region class

    Arguments
    ---------
    name : str
        Name of region
    longitude : float
        Longitude coordinate
    latitude : float
        Latitude coordinate
    fuel_disagg : dict
        Nested dict by region, enduse => np.array, single dimension for fuel type
    weather_regions : dict
        Weather regions

    Note
    ----
    *   The closest weather station is calculated
    """
    def __init__(
            self,
            name,
            longitude,
            latitude,
            region_fuel_disagg,
            weather_stations
        ):
        """Constructor
        """
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.fuels = region_fuel_disagg

        # Get closest weather station
        self.closest_weather_region_id = weather_station_location.get_closest_station(
            longitude,
            latitude,
            weather_stations)
