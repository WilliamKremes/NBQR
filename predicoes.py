import folium
from hazard_area import draw_hazard_area_generic
from espargimento import desenhar_area_espargimento, desenhar_area_espargimento2
from math import radians, degrees, sin, cos

# ------------------------
# Função para deslocamento aproximado em latitude/longitude
# ------------------------
def meters_to_latlon(lon, lat, distance, azimuth_deg):
    """
    Retorna o ponto final (lat, lon) deslocado 'distance' metros de (lat, lon)
    na direção 'azimuth_deg' (graus, norte=0, leste=90)
    """
    R = 6371000  # raio médio da Terra em metros
    az = radians(azimuth_deg)
    lat1 = radians(lat)
    lon1 = radians(lon)

    lat2 = sin(lat1) * cos(distance / R) + cos(lat1) * sin(distance / R) * cos(az)
    lat2 = degrees(lat1 + (distance / R) * cos(az))
    lon2 = degrees(lon1 + (distance / R) * sin(az) / cos(lat1))

    return lat2, lon2

# ------------------------
# Predição simplificada
# ------------------------
def executar_predicao_simplificada(map_obj, source, wind_speed, wind_direction):
    draw_hazard_area_generic(
        map_object=map_obj,
        source_location=source,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        radius_release_area=2000,
        downwind_distance=10000,
        common_length=12600,
        desenhar_poligono_condicional=False
    )

# ------------------------
# Parâmetros por estabilidade
# ------------------------
def obter_parametros_por_estabilidade(estabilidade_do_ar, meio_de_lancamento):
    meio = meio_de_lancamento.strip().lower()
    est = estabilidade_do_ar.strip().lower()

    if est == 'instável':
        if meio in ['submunição', 'granada', 'mina']:
            return 10000, 12000
        else:
            return 15000, 18000
    elif est == 'neutra':
        return 30000, 35200
    elif est == 'estável':
        return 50000, 58250
    else:
        print("Estabilidade do ar inválida. Usando padrão instável.")
        return 10000, 12000

# ------------------------
# Predição detalhada não persistente
# ------------------------
def executar_predicao_nao_persistente(map_obj, source, wind_speed, wind_direction):
    estabilidade_do_ar = input("Digite a estabilidade do ar (instável, neutra ou estável): ").strip().lower()
    meio_de_lancamento = input("Digite o meio de lançamento: ").strip().lower()

    downwind_distance, common_length = obter_parametros_por_estabilidade(estabilidade_do_ar, meio_de_lancamento)

    draw_hazard_area_generic(
        map_object=map_obj,
        source_location=source,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        radius_release_area=1000,
        downwind_distance=downwind_distance,
        common_length=common_length,
        meio_de_lancamento=meio_de_lancamento,
        estabilidade_do_ar=estabilidade_do_ar,
        desenhar_poligono_condicional=True
    )

# ------------------------
# Predição detalhada persistente
# ------------------------
def executar_predicao_persistente(map_obj, source, wind_speed, wind_direction):
    meio_de_lancamento = input("Digite o meio de lançamento: ").strip().lower()

    if meio_de_lancamento in ['espargimento', 'gerador']:
        source_final = (-22.841, -43.1798)
        downwind_distance = 10000
        common_length = 12000
        radius_release_area = 1000

        if wind_speed <= 10:
            desenhar_area_espargimento(
                map_obj=map_obj,
                source=source,
                source_final=source_final,
                radius_release_area=radius_release_area,
                downwind_distance=downwind_distance,
                common_length=common_length,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                meio_de_lancamento=meio_de_lancamento,
                draw_hazard_area_generic=draw_hazard_area_generic
            )
        else:
            desenhar_area_espargimento2(
                map_obj=map_obj,
                source=source,
                source_final=source_final,
                radius_release_area=radius_release_area,
                downwind_distance=downwind_distance,
                common_length=common_length,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                meio_de_lancamento=meio_de_lancamento,
                draw_hazard_area_generic=draw_hazard_area_generic
            )
    else:
        if meio_de_lancamento in ['bomba', 'granada', 'mina', 'foguete de detonação de superfície', 'míssil']:
            radius_release_area = 1000
            downwind_distance = 10000
            common_length = 12000
        elif meio_de_lancamento in ['foguete de detonação aérea', 'míssil de detonação aérea']:
            radius_release_area = 2000
            downwind_distance = 10000
            common_length = 12600
        else:
            print("Meio de lançamento não reconhecido. Usando padrão.")
            radius_release_area = 1000
            downwind_distance = 10000
            common_length = 12000

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

# ------------------------
# Wrappers HTTP
# ------------------------
def executar_predicao_nao_persistente_http(*args, **kwargs):
    return executar_predicao_nao_persistente(*args, **kwargs)

def executar_predicao_persistente_http(*args, **kwargs):
    return executar_predicao_persistente(*args, **kwargs)
