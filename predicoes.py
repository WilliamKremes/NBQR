%%writefile predicoes.py

import folium
from hazard_area import draw_hazard_area_generic
import math
from espargimento import desenhar_area_espargimento, desenhar_area_espargimento2


def executar_predicao_simplificada(map_obj, source, wind_speed, wind_direction):
    """Executa a predição simplificada com valores fixos."""
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


def obter_parametros_por_estabilidade(estabilidade_do_ar, meio_de_lancamento):
    """Retorna a distância downwind e common_length com base na estabilidade do ar e meio de lançamento."""
    meio = meio_de_lancamento.strip().lower()
    est = estabilidade_do_ar.strip().lower()

    if est == 'instável':
        if meio in ['submunição', 'granada', 'mina']:
            downwind_distance = 10000
            common_length = 12000
        else:
            downwind_distance = 15000
            common_length = 18000
    elif est == 'neutra':
        downwind_distance = 30000
        common_length = 35200
    elif est == 'estável':
        downwind_distance = 50000
        common_length = 58250
    else:
        print("Estabilidade do ar inválida. Usando valores padrão para instável.")
        downwind_distance = 10000
        common_length = 12000

    return downwind_distance, common_length


def executar_predicao_nao_persistente(map_obj, source, wind_speed, wind_direction,
                                      estabilidade_do_ar='instável', meio_de_lancamento='granada'):
    """Executa a predição detalhada para agentes não persistentes."""
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


def executar_predicao_persistente(map_obj, source, wind_speed, wind_direction,
                                  meio_de_lancamento='bomba', source_final=None):
    """Executa a predição detalhada para agentes persistentes."""

    # Casos de espargimento
    if meio_de_lancamento in ['espargimento', 'gerador']:
        if source_final is None:
            source_final = (-22.841, -43.1798)
        downwind_distance = 10000
        common_length = downwind_distance
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

    # Casos de outros meios
    else:
        # Para outros meios
        if meio_de_lancamento in ['bomba', 'granada', 'mina', 'foguete de detonação de superfície', 'míssil']:
            radius_release_area = 1000
            downwind_distance = 10000
            common_length = 12000
        elif meio_de_lancamento in ['foguete de detonação aérea', 'míssil de detonação aérea']:
            radius_release_area = 2000
            downwind_distance = 10000
            common_length = 12600
        else:
            print("Meio de lançamento não reconhecido. Usando valores padrão.")
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
