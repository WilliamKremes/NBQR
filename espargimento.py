

import folium
from math import radians, sin, cos, sqrt
from pyproj import Geod

# Inicializa geodésia WGS84
geod = Geod(ellps="WGS84")

def meters_to_latlon(lon, lat, distance, azimuth):
    """
    Retorna o ponto final (lat, lon) deslocado a 'distance' metros de (lat, lon)
    na direção 'azimuth' (graus, norte=0, leste=90).
    """
    lon2, lat2, _ = geod.fwd(lon, lat, azimuth, distance)
    return lat2, lon2


def desenhar_area_espargimento(
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
    """
    Desenha a área de espargimento para vento <= 10 km/h
    """
    # Desenhar áreas de liberação usando função genérica
    for ponto in [source, source_final]:
        draw_hazard_area_generic(
            map_object=map_obj,
            source_location=ponto,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            radius_release_area=radius_release_area,
            downwind_distance=downwind_distance,
            common_length=common_length,
            meio_de_lancamento=meio_de_lancamento,
            estabilidade_do_ar='',
            desenhar_poligono_condicional=True
        )

    # Linha central entre os centros de liberação
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.5,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # Vetor perpendicular para criar paralelas e polígono entre as áreas
    lat1, lon1 = source
    lat2, lon2 = source_final
    # Azimute entre os pontos
    fwd_azimuth, back_azimuth, distance = geod.inv(lon1, lat1, lon2, lat2)
    # Perpendicular: azimute ±90
    perp_azimuth = fwd_azimuth + 90

    # Offset de 1 km para criar linhas paralelas
    offset = 1000
    upper_start = meters_to_latlon(lon1, lat1, offset, perp_azimuth)
    upper_end   = meters_to_latlon(lon2, lat2, offset, perp_azimuth)
    lower_start = meters_to_latlon(lon1, lat1, offset, perp_azimuth + 180)
    lower_end   = meters_to_latlon(lon2, lat2, offset, perp_azimuth + 180)

    folium.PolyLine(locations=[upper_start, upper_end], color='red', weight=2, tooltip='Paralela superior').add_to(map_obj)
    folium.PolyLine(locations=[lower_start, lower_end], color='red', weight=2, tooltip='Paralela inferior').add_to(map_obj)

    folium.Polygon(
        locations=[upper_start, upper_end, lower_end, lower_start],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        tooltip='Polígono entre linhas paralelas'
    ).add_to(map_obj)


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
    """
    Desenha a área de espargimento para vento > 10 km/h
    incluindo linhas downwind e triângulos de dispersão
    """
    for ponto in [source, source_final]:
        # Círculos de liberação
        folium.Circle(
            location=ponto,
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.3,
            popup=f'Área de Liberação - {ponto}'
        ).add_to(map_obj)

    # Linha central entre os dois centros
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.5,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # Triângulos de dispersão para cada ponto
    for lat, lon in [source, source_final]:
        # Ponto downwind
        down_lat, down_lon = meters_to_latlon(lon, lat, downwind_distance, wind_direction)
        folium.PolyLine(
            locations=[(lat, lon), (down_lat, down_lon)],
            color='white',
            weight=0.1,
            dash_array='5,5'
        ).add_to(map_obj)

        # Ponto perpendicular para criar triângulo
        side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
        # Perpendicular à linha do vento
        upper_lat, upper_lon = meters_to_latlon(down_lon, down_lat, side_length/2, wind_direction + 90)
        lower_lat, lower_lon = meters_to_latlon(down_lon, down_lat, side_length/2, wind_direction - 90)

        # Linhas triangulares
        for angle_offset, color, start_point in zip([60, 120], ['blue', 'green'], [(upper_lat, upper_lon), (lower_lat, lower_lon)]):
            end_lat, end_lon = meters_to_latlon(start_point[1], start_point[0], common_length, wind_direction - angle_offset)
            folium.PolyLine(
                locations=[start_point, (end_lat, end_lon)],
                color=color,
                weight=1,
                dash_array='5,5'
            ).add_to(map_obj)

        # Polígono triângulo final
        folium.Polygon(
            locations=[(upper_lat, upper_lon), (down_lat, down_lon), (lower_lat, lower_lon)],
            color='red',
            weight=2,
            fill=True,
            fill_opacity=0.2
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
