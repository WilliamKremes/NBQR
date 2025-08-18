from math import cos, radians

def meters_to_latlon_distances(meters, lat):
    """Converte deslocamento em metros para graus de latitude e longitude
    considerando a latitude atual (em graus)."""
    delta_lat = meters / 111320.0  # metros para graus latitude
    delta_lon = meters / (40075000.0 * cos(radians(lat)) / 360.0)  # metros para graus longitude
    return delta_lat, delta_lon
