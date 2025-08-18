# utils/geodesy.py
from pyproj import Geod

geod = Geod(ellps="WGS84")

def meters_to_latlon_distances(meters, lat, azimuth=0):
    """
    Calcula deslocamento em graus de latitude e longitude a partir
    de um deslocamento em metros e azimute em graus.

    Parâmetros:
        meters (float): distância em metros
        lat (float): latitude de referência em graus
        azimuth (float): direção do deslocamento em graus (0=norte, 90=leste)
    
    Retorna:
        tuple: (delta_lat, delta_lon) em graus
    """
    # Ponto inicial fictício (lon0 irrelevante)
    lon0, lat0 = 0, lat
    lon1, lat1, _ = geod.fwd(lon0, lat0, azimuth, meters)
    delta_lat = lat1 - lat0
    delta_lon = lon1 - lon0
    return delta_lat, delta_lon
