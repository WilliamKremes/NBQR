import folium
from math import radians, sin, cos, sqrt
from utils import meters_to_latlon_distances

def draw_hazard_area_generic(
    map_object,
    source_location,
    wind_speed,
    wind_direction,
    radius_release_area,
    downwind_distance,
    common_length,
    meio_de_lancamento=None,
    estabilidade_do_ar=None,
    desenhar_poligono_condicional=False
):
    lat, lon = source_location

    # Área de liberação (círculo)
    folium.Circle(
        location=source_location,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f'Área de Liberação ({radius_release_area / 1000:.1f} km)'
    ).add_to(map_object)

    # Ponto da fonte do incidente
    folium.CircleMarker(
        location=source_location,
        radius=1,
        color='black',
        fill=True,
        fill_opacity=1,
        popup='Fonte do Incidente'
    ).add_to(map_object)

    # Caso vento ≤ 10 km/h
    if wind_speed <= 10:
        folium.Circle(
            location=source_location,
            radius=10000,
            color='red',
            fill=True,
            fill_opacity=0.2,
            popup='Área de Perigo (10 km)'
        ).add_to(map_object)
        return

    # Verificação para desenho condicional
    if desenhar_poligono_condicional and (meio_de_lancamento is None or estabilidade_do_ar is None):
        raise ValueError("meio_de_lancamento e estabilidade_do_ar são obrigatórios")

    # ----------------------
    # Ponto downwind (na direção do vento)
    # ----------------------
    delta_lat_dw, delta_lon_dw = meters_to_latlon_distances(downwind_distance, lat)
    # Ajusta direção do vento (0=norte, 90=leste)
    azimuth_rad = radians(wind_direction)
    lat_dw = lat + delta_lat_dw * sin(azimuth_rad)
    lon_dw = lon + delta_lon_dw * cos(azimuth_rad)
    downwind_point = (lat_dw, lon_dw)

    folium.PolyLine(
        [source_location, downwind_point],
        color='white',
        weight=0.1,
        dash_array='5,5'
    ).add_to(map_object)

    # ----------------------
    # Reta perpendicular ao vento (para polígono)
    # ----------------------
    side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
    perp_angle_rad = radians((wind_direction + 90) % 360)

    delta_lat_up, delta_lon_up = meters_to_latlon_distances(side_length / 2, lat_dw)
    delta_lat_down, delta_lon_down = meters_to_latlon_distances(side_length / 2, lat_dw)

    lat_up = lat_dw + delta_lat_up * sin(perp_angle_rad)
    lon_up = lon_dw + delta_lon_up * cos(perp_angle_rad)
    lat_down = lat_dw - delta_lat_down * sin(perp_angle_rad)
    lon_down = lon_dw - delta_lon_down * cos(perp_angle_rad)

    upper_perpendicular = (lat_up, lon_up)
    lower_perpendicular = (lat_down, lon_down)

    folium.PolyLine(
        [upper_perpendicular, lower_perpendicular],
        color='black',
        weight=1,
        dash_array='5,5'
    ).add_to(map_object)

    # ----------------------
    # Função para desenhar linhas coloridas
    # ----------------------
    def draw_line(start_point, azimuth_deg, length, color):
        azimuth_rad = radians(azimuth_deg)
        delta_lat, delta_lon = meters_to_latlon_distances(length, start_point[0])
        lat_end = start_point[0] + delta_lat * sin(azimuth_rad)
        lon_end = start_point[1] + delta_lon * cos(azimuth_rad)
        folium.PolyLine(
            [start_point, (lat_end, lon_end)],
            color=color,
            weight=1,
            dash_array='5,5'
        ).add_to(map_object)
        return (lat_end, lon_end)

    # Linhas azuis e verdes (60° e 120° em relação à perpendicular)
    blue_end = draw_line(upper_perpendicular, (wind_direction + 30) % 360, common_length, 'blue')
    green_end = draw_line(lower_perpendicular, (wind_direction - 30) % 360, common_length, 'green')

    # Linha final amarelo (entre os pontos finais)
    folium.PolyLine(
        [blue_end, green_end],
        color='yellow',
        weight=1,
        dash_array='5,5'
    ).add_to(map_object)

    # ----------------------
    # Polígono fechado
    # ----------------------
    folium.Polygon(
        [upper_perpendicular, blue_end, green_end, lower_perpendicular],
        color='red',
        weight=2,
        fill=True,
        fill_opacity=0.2,
        popup='Polígono Fechado'
    ).add_to(map_object)

    # Círculo reforçado da área de liberação
    folium.Circle(
        location=source_location,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup='Área de Liberação'
    ).add_to(map_object)
