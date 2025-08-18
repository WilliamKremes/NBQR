import math
from math import radians, cos, sin, sqrt
import folium
from utils import meters_to_latlon_distances


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
    draw_hazard_area_generic(
        map_object=map_obj,
        source_location=source,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        radius_release_area=radius_release_area,
        downwind_distance=downwind_distance,
        common_length=common_length,
        meio_de_lancamento=meio_de_lancamento,
        estabilidade_do_ar='',
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
        estabilidade_do_ar='',
        desenhar_poligono_condicional=True
    )

    # Círculo para a segunda área de liberação
    folium.Circle(
        location=source_final,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup='Área de Liberação - source_final'
    ).add_to(map_obj)

    # Linha central entre os dois centros de liberação
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

    # Distância perpendicular em metros
    offset_metros = 1000
    dlat_m = offset_metros * perp_dy
    dlon_m = offset_metros * perp_dx

    # Converter deslocamento para coordenadas geográficas
    delta_lat, _ = meters_to_latlon_distances(dlat_m, (lat1 + lat2)/2)
    _, delta_lon = meters_to_latlon_distances(dlon_m, (lat1 + lat2)/2)

    # Linha paralela superior
    p1_sup = (lat1 + delta_lat, lon1 + delta_lon)
    p2_sup = (lat2 + delta_lat, lon2 + delta_lon)
    folium.PolyLine(
        locations=[p1_sup, p2_sup],
        color='red',
        weight=2,
        tooltip='Paralela superior'
    ).add_to(map_obj)

    # Linha paralela inferior
    p2_inf = (lat2 - delta_lat, lon2 - delta_lon)
    p1_inf = (lat1 - delta_lat, lon1 - delta_lon)
    folium.PolyLine(
        locations=[p1_inf, p2_inf],
        color='red',
        weight=2,
        tooltip='Paralela inferior'
    ).add_to(map_obj)

    # Polígono de espargimento entre as linhas paralelas
    folium.Polygon(
        locations=[p1_sup, p2_sup, p2_inf, p1_inf],
        color='red',
        weight=2,
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        tooltip='Polígono entre linhas paralelas'
    ).add_to(map_obj)


    # Distância perpendicular em metros
    offset_metros = 10000
    dlat_m1 = offset_metros * perp_dy
    dlon_m1 = offset_metros * perp_dx

    # Converter deslocamento para coordenadas geográficas
    delta_lat1, _ = meters_to_latlon_distances(dlat_m1, (lat1 + lat2)/2)
    _, delta_lon1 = meters_to_latlon_distances(dlon_m1, (lat1 + lat2)/2)

    # Linha paralela superior
    p11_sup = (lat1 + delta_lat1, lon1 + delta_lon1)
    p22_sup = (lat2 + delta_lat1, lon2 + delta_lon1)
    folium.PolyLine(
        locations=[p11_sup, p22_sup],
        color='red',
        weight=2,
        tooltip='Paralela superior'
    ).add_to(map_obj)

    # Linha paralela inferior
    p22_inf = (lat2 - delta_lat1, lon2 - delta_lon1)
    p11_inf = (lat1 - delta_lat1, lon1 - delta_lon1)
    folium.PolyLine(
        locations=[p11_inf, p22_inf],
        color='red',
        weight=2,
        tooltip='Paralela inferior'
    ).add_to(map_obj)

    # Polígono de espargimento entre as linhas paralelas
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
    draw_hazard_area_generic
):
    # 1. Desenha os círculos das áreas de liberação
    folium.Circle(
        location=source,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.3,
        popup='Área de Liberação - source'
    ).add_to(map_obj)

    folium.Circle(
        location=source_final,
        radius=radius_release_area,
        color='red',
        fill=True,
        fill_opacity=0.3,
        popup='Área de Liberação - source_final'
    ).add_to(map_obj)

    # 2. Linha central entre os dois centros
    folium.PolyLine(
        locations=[source, source_final],
        color='gray',
        weight=0.1,
        tooltip='Linha entre áreas de liberação'
    ).add_to(map_obj)

    # 3. Calcular vetor perpendicular para linhas paralelas e polígono entre eles
    lat1, lon1 = source
    lat2, lon2 = source_final
    dx = lon2 - lon1
    dy = lat2 - lat1
    comprimento = math.sqrt(dx**2 + dy**2)
    if comprimento == 0:
        return  # Evita divisão por zero

    perp_dx = -dy / comprimento
    perp_dy = dx / comprimento

    offset_metros = 1000  # Distância perpendicular 1 km
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

    # 4. Para cada ponto (source e source_final) desenhar downwind e triângulos
    angle_rad = radians(wind_direction)

    for lat, lon in [source, source_final]:
        # Calcular ponto downwind na direção do vento
        delta_lat_m = downwind_distance * sin(angle_rad)
        delta_lon_m = downwind_distance * cos(angle_rad)

        delta_lat_deg, _ = meters_to_latlon_distances(delta_lat_m, lat)
        _, delta_lon_deg = meters_to_latlon_distances(delta_lon_m, lat)

        downwind_point = (lat + delta_lat_deg, lon + delta_lon_deg)

        # Linha branca tracejada do círculo até downwind_point
        folium.PolyLine(
            locations=[(lat, lon), downwind_point],
            color='white',
            weight=0.1,
            dash_array='5,5',
        ).add_to(map_obj)

        # Calcular linhas perpendiculares e triângulos
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
        ).add_to(map_obj)

        def draw_line(start_point, base_angle, angle_offset_deg, color, length):
            angle = base_angle - radians(angle_offset_deg)
            delta_lat_line, delta_lon_line = meters_to_latlon_distances(length, lat)
            end_point = (
                start_point[0] - delta_lat_line * sin(angle),
                start_point[1] - delta_lon_line * cos(angle)
            )
            folium.PolyLine(
                locations=[start_point, end_point],
                color=color,
                weight=1,
                dash_array='5,5'
            ).add_to(map_obj)

        # Desenha linhas azul e verde formando os triângulos
        for angle_offset, color, start_pt in zip([60, 120], ['blue', 'green'], [upper_perpendicular, lower_perpendicular]):
            common_length = 12000
            draw_line(start_pt, perp_angle, angle_offset, color, common_length)

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
        ).add_to(map_obj)

        # Polígono fechado do triângulo
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
        ).add_to(map_obj)



        # Círculo reforçado da área de liberação (opcional)
        folium.Circle(
            location=(lat, lon),
            radius=radius_release_area,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup='Área de Liberação'
        ).add_to(map_obj)
