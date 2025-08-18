from pyproj import Geod

geod = Geod(ellps="WGS84")

def meters_to_latlon_distances(meters, lat, azimuth=0):
    """
    Calcula deslocamento em graus de latitude e longitude a partir
    de um deslocamento em metros e azimute em graus.
    """
    # Azimuth 0 = norte, 90 = leste
    lon0, lat0, _ = 0, lat, 0  # lat base, lon base irrelevante para delta
    lon1, lat1, _ = geod.fwd(lon0, lat0, azimuth, meters)
    delta_lat = lat1 - lat0
    delta_lon = lon1 - lon0
    return delta_lat, delta_lon
