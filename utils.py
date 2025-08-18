from pyproj import Geod

# Inicializa geodésia WGS84
geod = Geod(ellps="WGS84")

def meters_to_latlon(lon, lat, distance_m, azimuth_deg):
    """
    Calcula o ponto final a partir de um ponto inicial (lon, lat),
    distância em metros e azimute em graus.
    
    Parâmetros:
        lon (float): longitude inicial em graus
        lat (float): latitude inicial em graus
        distance_m (float): deslocamento em metros
        azimuth_deg (float): direção do deslocamento (0=norte, 90=leste)
    
    Retorna:
        tuple: (latitude, longitude) do ponto final
    """
    lon1, lat1, _ = geod.fwd(lon, lat, azimuth_deg, distance_m)
    return lat1, lon1
