import math
from math import radians, sin, cos, sqrt
import folium
from pyproj import Geod

geod = Geod(ellps="WGS84")

def meters_to_latlon_distances(meters, lat, azimuth):
    """
    Converte deslocamento em metros para graus de latitude e longitude
    considerando a latitude atual e a direção (azimute) do deslocamento.
    """
    lon0, lat0 = 0, lat
    lon1, lat1, _ = geod.fwd(lon0, lat0, azimuth, meters)
    delta_lat = lat1 - lat0
    delta_lon = lon1 - lon0
    return delta_lat, delta_lon


def desenhar_area_espargimento2(
    map_obj,
    source,
    source_final,
    wind_speed,
    wind_direction,
    radius_release_area,
    downwind_distance,
    common_length,
    meio_de_lancamento,
    draw_hazard_area_generic
):
    # 1. Desenha os círculos das áreas de liberação
    for loc, label in zip([source, source_final], ['source', 'source_final']):
        folium.Circle(
            location=loc,
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.3,
            popup=f'Área de Liberação - {label}'
        ).add_to(map_obj)

    # 2. Linha central entre os dois centros
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.1,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # 3. Vetor perpendicular para linhas paralelas
    lat1, lon1 = source
    lat2, lon2 = source_final
    dx = lon2 - lon1
    dy = lat2 - lat1
    comprimento = sqrt(dx**2 + dy**2)
    if comprimento == 0:
        return

    perp_dx = -dy / comprimento
    perp_dy = dx / comprimento

    offset_metros = 1000  # 1 km
    azimuth_perp = math.degrees(math.atan2(perp_dx, perp_dy))
    delta_lat, delta_lon = meters_to_latlon_distances(offset_metros, (lat1 + lat2)/2, azimuth_perp)

    p1_sup = (lat1 + delta_lat, lon1 + delta_lon)
    p2_sup = (lat2 + delta_lat, lon2 + delta_lon)
    p1_inf = (lat1 - delta_lat, lon1 - delta_lon)
    p2_inf = (lat2 - delta_lat, lon2 - delta_lon)

    folium.PolyLine([p1_sup, p2_sup], color='red', weight=2, tooltip='Paralela superior').add_to(map_obj)
    folium.PolyLine([p1_inf, p2_inf], color='red', weight=2, tooltip='Paralela inferior').add_to(map_obj)

    folium.Polygon(
        locations=[p1_sup, p2_sup, p2_inf, p1_inf],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.3,
        tooltip='Polígono entre linhas paralelas'
    ).add_to(map_obj)

    # 4. Downwind e triângulos para cada ponto
    angle_rad = radians(wind_direction)

    for lat, lon in [source, source_final]:
        # Ponto downwind
        delta_lat_m = downwind_distance * sin(angle_rad)
        delta_lon_m = downwind_distance * cos(angle_rad)
        delta_lat_deg, delta_lon_deg = meters_to_latlon_distances(
            sqrt(delta_lat_m**2 + delta_lon_m**2),
            lat,
            math.degrees(math.atan2(delta_lon_m, delta_lat_m))
        )
        downwind_point = (lat + delta_lat_deg, lon + delta_lon_deg)

        # Linha branca tracejada do círculo até downwind_point
        folium.PolyLine(
            locations=[(lat, lon), downwind_point],
            color='white',
            weight=0.1,
            dash_array='5,5',
        ).add_to(map_obj)

        # Triângulo lateral
        side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
        perp_angle = angle_rad + radians(90)

        delta_lat_latlon, delta_lon_latlon = meters_to_latlon_distances(
            side_length / 2,
            downwind_point[0],
            math.degrees(perp_angle)
        )

        upper_perp = (downwind_point[0] + delta_lat_latlon, downwind_point[1] + delta_lon_latlon)
        lower_perp = (downwind_point[0] - delta_lat_latlon, downwind_point[1] - delta_lon_latlon)

        folium.PolyLine([upper_perp, lower_perp], color='black', weight=1, dash_array='5,5').add_to(map_obj)

        # Linhas azul e verde formando triângulos
        def draw_line(start_point, base_angle_rad, angle_offset_deg, color, length):
            angle = base_angle_rad - radians(angle_offset_deg)
            delta_lat_line, delta_lon_line = meters_to_latlon_distances(length, start_point[0], math.degrees(angle))
            end_point = (start_point[0] - delta_lat_line, start_point[1] - delta_lon_line)
            folium.PolyLine([start_point, end_point], color=color, weight=1, dash_array='5,5').add_to(map_obj)
            return end_point

        blue_end = draw_line(upper_perp, perp_angle, 60, 'blue', common_length)
        green_end = draw_line(lower_perp, perp_angle, 120, 'green', common_length)

        # Linha entre pontas azul e verde
        folium.PolyLine([blue_end, green_end], color='yellow', weight=1, dash_array='5,5').add_to(map_obj)

        # Polígono fechado do triângulo
        folium.Polygon(
            locations=[upper_perp, blue_end, green_end, lower_perp],
            color='red',
            weight=2,
            fill=True,
            fill_opacity=0.2,
            popup='Polígono Fechado'
        ).add_to(map_obj)

        # Círculo reforçado da área de liberação
        folium.Circle(
            location=(lat, lon),
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup='Área de Liberação'
        ).add_to(map_obj)
