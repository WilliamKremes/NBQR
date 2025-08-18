import math
from math import radians, sin, sqrt
import folium
from utils import meters_to_latlon_distances
from hazard_area import draw_hazard_area_generic

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
    draw_hazard_area_generic=draw_hazard_area_generic
):
    # Desenha duas áreas com a rotina genérica
    draw_hazard_area_generic(
        map_object=map_obj,
        source_location=source,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        radius_release_area=radius_release_area,
        downwind_distance=downwind_distance,
        common_length=common_length,
        meio_de_lancamento=meio_de_lancamento,
        estabilidade_do_ar='instável',
        desenhar_poligono_condicional=True
    )

    draw_hazard_area_generic(
        map_object=map_obj,
        source_location=source_final,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        radius_release_area=radius_release_area,
        downwind_distance=downwind_distance,
        common_length=common_length,
        meio_de_lancamento=meio_de_lancamento,
        estabilidade_do_ar='instável',
        desenhar_poligono_condicional=True
    )

    # Marca a segunda área de liberação
    folium.Circle(
        location=source_final,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup='Área de Liberação - source_final'
    ).add_to(map_obj)

    # Linha central entre os dois centros
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.1,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # Calcular vetor perpendicular
    lat1, lon1 = source
    lat2, lon2 = source_final
    dx = lon2 - lon1
    dy = lat2 - lat1
    comprimento = math.sqrt(dx**2 + dy**2)
    if comprimento == 0:
        return

    # Vetor perpendicular normalizado
    perp_dx = -dy / comprimento
    perp_dy = dx / comprimento

    # 1 km de offset
    offset_metros = 1000
    dlat_m = offset_metros * perp_dy
    dlon_m = offset_metros * perp_dx

    # Converter deslocamento para coordenadas geográficas
    delta_lat, _ = meters_to_latlon_distances(dlat_m, (lat1 + lat2)/2)
    _, delta_lon = meters_to_latlon_distances(dlon_m, (lat1 + lat2)/2)

    # Linhas paralelas superior e inferior
    p1_sup = (lat1 + delta_lat, lon1 + delta_lon)
    p2_sup = (lat2 + delta_lat, lon2 + delta_lon)
    p2_inf = (lat2 - delta_lat, lon2 - delta_lon)
    p1_inf = (lat1 - delta_lat, lon1 - delta_lon)

    folium.PolyLine(locations=[p1_sup, p2_sup], color='red', weight=2, tooltip='Paralela superior').add_to(map_obj)
    folium.PolyLine(locations=[p1_inf, p2_inf], color='red', weight=2, tooltip='Paralela inferior').add_to(map_obj)

    # Polígono de espargimento (1 km)
    folium.Polygon(
        locations=[p1_sup, p2_sup, p2_inf, p1_inf],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        tooltip='Polígono entre linhas paralelas'
    ).add_to(map_obj)

    # 10 km de offset (faixa mais larga e suave)
    offset_metros = 10000
    dlat_m1 = offset_metros * perp_dy
    dlon_m1 = offset_metros * perp_dx

    delta_lat1, _ = meters_to_latlon_distances(dlat_m1, (lat1 + lat2)/2)
    _, delta_lon1 = meters_to_latlon_distances(dlon_m1, (lat1 + lat2)/2)

    p11_sup = (lat1 + delta_lat1, lon1 + delta_lon1)
    p22_sup = (lat2 + delta_lat1, lon2 + delta_lon1)
    folium.PolyLine(
        locations=[p11_sup, p22_sup],
        color='red',
        weight=2,
        tooltip='Paralela superior'
    ).add_to(map_obj)

    p22_inf = (lat2 - delta_lat1, lon2 - delta_lon1)
    p11_inf = (lat1 - delta_lat1, lon1 - delta_lon1)
    folium.PolyLine(
        locations=[p11_inf, p22_inf],
        color='red',
        weight=2,
        tooltip='Paralela inferior'
    ).add_to(map_obj)

    folium.Polygon(
        locations=[p11_sup, p22_sup, p22_inf, p11_inf],
        color='red',
        weight=0.01,
        fill=True,
        fill_color='red',
        fill_opacity=0.08,
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
    draw_hazard_area_generic=draw_hazard_area_generic
):
    # 1) Círculos das áreas de liberação
    folium.Circle(location=source, radius=radius_release_area, color='red', fill=True, fill_opacity=0.3,
                  popup='Área de Liberação - source').add_to(map_obj)
    folium.Circle(location=source_final, radius=radius_release_area, color='red', fill=True, fill_opacity=0.3,
                  popup='Área de Liberação - source_final').add_to(map_obj)

    # 2) Linha central
    folium.PolyLine(locations=[source, source_final], color='gray', weight=0.1,
                    tooltip='Linha entre áreas de liberação').add_to(map_obj)

    # 3) Perpendiculares e polígono entre faixas
    lat1, lon1 = source
    lat2, lon2 = source_final
    dx = lon2 - lon1
    dy = lat2 - lat1
    comprimento = math.sqrt(dx**2 + dy**2)
    if comprimento == 0:
        return

    perp_dx = -dy / comprimento
    perp_dy = dx / comprimento

    offset_metros = 1000  # 1 km
    dlat_m = offset_metros * perp_dy
    dlon_m = offset_metros * perp_dx

    delta_lat, _ = meters_to_latlon_distances(dlat_m, (lat1 + lat2)/2)
    _, delta_lon = meters_to_latlon_distances(dlon_m, (lat1 + lat2)/2)

    p1_sup = (lat1 + delta_lat, lon1 + delta_lon)
    p2_sup = (lat2 + delta_lat, lon2 + delta_lon)
    p2_inf = (lat2 - delta_lat, lon2 - delta_lon)
    p1_inf = (lat1 - delta_lat, lon1 - delta_lon)

    folium.PolyLine(locations=[p1_sup, p2_sup], color='red', weight=2, tooltip='Paralela superior').add_to(map_obj)
    folium.PolyLine(locations=[p1_inf, p2_inf], color='red', weight=2, tooltip='Paralela inferior').add_to(map_obj)

    folium.Polygon(
        locations=[p1_sup, p2_sup, p2_inf, p1_inf],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.3,
        tooltip='Polígono entre linhas paralelas'
    ).add_to(map_obj)

    # 4) Para cada ponto, desenhar downwind e triângulos
    angle_rad = radians(wind_direction)

    for lat, lon in [source, source_final]:
        # Ponto downwind
        delta_lat_m = downwind_distance * sin(angle_rad)
        delta_lon_m = downwind_distance * 1.0  # cos() omitido; usamos fator unitário para simplificar
        delta_lat_deg, _ = meters_to_latlon_distances(delta_lat_m, lat)
        _, delta_lon_deg = meters_to_latlon_distances(delta_lon_m, lat)
        downwind_point = (lat + delta_lat_deg, lon + delta_lon_deg)

        folium.PolyLine(locations=[(lat, lon), downwind_point], color='white', weight=0.1, dash_array='5,5').add_to(map_obj)

        side_length = (2 / sqrt(3)) * (downwind_distance + 2 * radius_release_area)
        perp_angle = angle_rad + radians(90)
        delta_perp_lat, delta_perp_lon = meters_to_latlon_distances(side_length / 2, lat)

        upper_perpendicular = (
            downwind_point[0] + delta_perp_lat * sin(perp_angle),
            downwind_point[1] + delta_perp_lon * 1.0
        )
        lower_perpendicular = (
            downwind_point[0] - delta_perp_lat * sin(perp_angle),
            downwind_point[1] - delta_perp_lon * 1.0
        )

        folium.PolyLine(locations=[upper_perpendicular, lower_perpendicular], color='black', weight=1,
                        dash_array='5,5').add_to(map_obj)

        def draw_line(start_point, base_angle, angle_offset_deg, color, length):
            ang = base_angle - radians(angle_offset_deg)
            dlat_line, dlon_line = meters_to_latlon_distances(length, lat)
            end_point = (start_point[0] - dlat_line * sin(ang), start_point[1] - dlon_line * 1.0)
            folium.PolyLine(locations=[start_point, end_point], color=color, weight=1,
                            dash_array='5,5').add_to(map_obj)

        for angle_offset, color, start_pt in zip([60, 120], ['blue', 'green'], [upper_perpendicular, lower_perpendicular]):
            common_len = 12000
            draw_line(start_pt, perp_angle, angle_offset, color, common_len)

        dblue_lat, dblue_lon = meters_to_latlon_distances(12000, lat)
        blue_end_point = (
            upper_perpendicular[0] - dblue_lat * sin(perp_angle - radians(60)),
            upper_perpendicular[1] - dblue_lon * 1.0
        )
        green_end_point = (
            lower_perpendicular[0] - dblue_lat * sin(perp_angle - radians(120)),
            lower_perpendicular[1] - dblue_lon * 1.0
        )

        folium.PolyLine(locations=[blue_end_point, green_end_point], color='yellow', weight=1,
                        dash_array='5,5').add_to(map_obj)

        folium.Polygon(
            locations=[upper_perpendicular, blue_end_point, green_end_point, lower_perpendicular],
            color='red',
            weight=2,
            fill=True,
            fill_opacity=0.2,
            popup='Polígono Fechado'
        ).add_to(map_obj)
