import folium
from math import radians, sin, cos, sqrt
from utils import meters_to_latlon_distances  # função do utils.py

def move_point(lat, lon, distance_m, azimuth_deg):
    """
    Retorna ponto (lat, lon) deslocado 'distance_m' metros na direção 'azimuth_deg'
    """
    delta_lat, delta_lon = meters_to_latlon_distances(distance_m, lat)
    az = radians(azimuth_deg)
    lat_new = lat + delta_lat * sin(az)
    lon_new = lon + delta_lon * cos(az)
    return lat_new, lon_new


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
    Área de espargimento para vento <= 10 km/h
    """
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

    # Linha central
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.5,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # Paralelas (1 km de offset)
    offset = 1000
    lat1, lon1 = source
    lat2, lon2 = source_final

    upper_start = move_point(lat1, lon1, offset, 90)
    upper_end   = move_point(lat2, lon2, offset, 90)
    lower_start = move_point(lat1, lon1, offset, 270)
    lower_end   = move_point(lat2, lon2, offset, 270)

    folium.PolyLine([upper_start, upper_end], color='red', weight=2).add_to(map_obj)
    folium.PolyLine([lower_start, lower_end], color='red', weight=2).add_to(map_obj)

    folium.Polygon(
        [upper_start, upper_end, lower_end, lower_start],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.7
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
    Área de espargimento para vento > 10 km/h
    """
    for ponto in [source, source_final]:
        folium.Circle(
            location=ponto,
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.3
        ).add_to(map_obj)

    # Linha central
    folium.PolyLine([source, source_final], color='gray', weight=0.5).add_to(map_obj)

    for lat, lon in [source, source_final]:
        # Ponto downwind
        down_lat, down_lon = move_point(lat, lon, downwind_distance, wind_direction)
        folium.PolyLine([(lat, lon), (down_lat, down_lon)],
                        color='white', weight=0.1, dash_array='5,5').add_to(map_obj)

        # Perpendicular (triângulo)
        side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
        upper_lat, upper_lon = move_point(down_lat, down_lon, side_length/2, wind_direction + 90)
        lower_lat, lower_lon = move_point(down_lat, down_lon, side_length/2, wind_direction - 90)

        # Linhas coloridas
        blue_end_lat, blue_end_lon = move_point(upper_lat, upper_lon, common_length, wind_direction - 60)
        green_end_lat, green_end_lon = move_point(lower_lat, lower_lon, common_length, wind_direction - 120)

        folium.PolyLine([(upper_lat, upper_lon), (blue_end_lat, blue_end_lon)],
                        color='blue', weight=1, dash_array='5,5').add_to(map_obj)
        folium.PolyLine([(lower_lat, lower_lon), (green_end_lat, green_end_lon)],
                        color='green', weight=1, dash_array='5,5').add_to(map_obj)

        folium.Polygon(
            [(upper_lat, upper_lon), (blue_end_lat, blue_end_lon),
             (green_end_lat, green_end_lon), (lower_lat, lower_lon)],
            color='red', weight=2, fill=True, fill_opacity=0.2
        ).add_to(map_obj)

        folium.Circle(
            location=(lat, lon),
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.7
        ).add_to(map_obj)
