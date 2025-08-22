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
        popup=f'Área de Liberação ({radius_release_area / 1000} km)'
    ).add_to(map_object)

    # Ponto da fonte do incidente
    folium.CircleMarker(
        location=source_location,
        radius=1,
        color='black',
        fill=True,
        fill_color='black',
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

    # Verifica condições para desenho condicional
    if desenhar_poligono_condicional:
      if meio_de_lancamento is None or estabilidade_do_ar is None:
        raise ValueError("meio_de_lancamento e estabilidade_do_ar são obrigatórios")
    
   angle_rad = radians(wind_direction)

    # Ponto downwind a distância na direção do vento
    delta_lat, delta_lon = meters_to_latlon_distances(downwind_distance, lat)
    downwind_point = (
        lat + delta_lat * sin(angle_rad),
        lon + delta_lon * cos(angle_rad)
    )

    # Linha fonte → ponto downwind
    folium.PolyLine(
        locations=[source_location, downwind_point],
        color='white',
        weight=0.1,
        dash_array='5,5',
    ).add_to(map_object)

    side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
    perp_angle = angle_rad + radians(90)
    delta_perp_lat, delta_perp_lon = meters_to_latlon_distances(side_length / 2, lat)

    upper_perpendicular = (
        downwind_point[0] + delta_perp_lat * sin(perp_angle),
        downwind_point[1] + delta_perp_lon * cos(perp_angle)
    )
    lower_perpendicular = (
        downwind_point[0] - delta_perp_lat * sin(perp_angle),
        downwind_point[1] - delta_perp_lon * cos(perp_angle)
    )

    folium.PolyLine(
        locations=[upper_perpendicular, lower_perpendicular],
        color='black',
        weight=1,
        dash_array='5,5',
    ).add_to(map_object)

    def draw_line(start_point, base_angle, angle_offset_deg, color, length):
        angle = base_angle - radians(angle_offset_deg)
        delta_lat, delta_lon = meters_to_latlon_distances(length, lat)
        end_point = (
            start_point[0] - delta_lat * sin(angle),
            start_point[1] - delta_lon * cos(angle)
        )
        folium.PolyLine(
            locations=[start_point, end_point],
            color=color,
            weight=1,
            dash_array='5,5'
        ).add_to(map_object)

    # Linhas azuis e verdes
    for angle_offset, color, start_pt in zip([60, 120], ['blue', 'green'], [upper_perpendicular, lower_perpendicular]):
        draw_line(start_pt, perp_angle, angle_offset, color, common_length)

    # Pontos finais polígono amarelo
    delta_blue_lat, delta_blue_lon = meters_to_latlon_distances(common_length, lat)
    blue_end_point = (
        upper_perpendicular[0] - delta_blue_lat * sin(perp_angle - radians(60)),
        upper_perpendicular[1] - delta_blue_lon * cos(perp_angle - radians(60))
    )
    green_end_point = (
        lower_perpendicular[0] - delta_blue_lat * sin(perp_angle - radians(120)),
        lower_perpendicular[1] - delta_blue_lon * cos(perp_angle - radians(120))
    )

    folium.PolyLine(
        locations=[blue_end_point, green_end_point],
        color='yellow',
        weight=1,
        dash_array='5,5'
    ).add_to(map_object)

    # Polígono fechado
    folium.Polygon(
        locations=[
            upper_perpendicular,
            blue_end_point,
            green_end_point,
            lower_perpendicular
        ],
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
