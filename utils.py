from math import cos, radians

def meters_to_latlon_distances(meters, lat):
    """
    Converte deslocamento em metros para graus de latitude e longitude,
    aproximando para pequenas distâncias.
    
    Parâmetros:
        meters (float): distância em metros
        lat (float): latitude atual em graus (para correção de longitude)
    
    Retorna:
        tuple: (delta_lat, delta_lon) em graus
    """
    delta_lat = meters / 111320  # aproximadamente metros por grau latitude
    delta_lon = meters / (40075000 * cos(radians(lat))/360)  # ajusta longitude pela latitude
    return delta_lat, delta_lon


