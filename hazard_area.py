

import folium
from pyproj import Geod
from math import sqrt

# Inicializa geodésia WGS84
geod = Geod(ellps="WGS84")

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
    lat_dw, lon_dw, _ = geod.fwd(lon, lat, wind_direction, downwind_distance)
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
    perp_angle = (wind_direction + 90) % 360

    lat_up, lon_up, _ = geod.fwd(lon_dw, lat_dw, perp_angle, side_length / 2)
    lat_down, lon_down, _ = geod.fwd(lon_dw, lat_dw, (perp_angle + 180) % 360, side_length / 2)
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
        lat_end, lon_end, _ = geod.fwd(start_point[1], start_point[0], azimuth_deg, length)
        folium.PolyLine(
            [start_point, (lat_end, lon_end)],
            color=color,
            weight=1,
            dash_array='5,5'
        ).add_to(map_object)
        return (lat_end, lon_end)

    # Linhas azuis e verdes (60° e 120° em relação à perpendicular)
    blue_end = draw_line(upper_perpendicular, (perp_angle - 60) % 360, common_length, 'blue')
    green_end = draw_line(lower_perpendicular, (perp_angle - 120) % 360, common_length, 'green')

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
