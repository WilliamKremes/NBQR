from flask import Flask, request, render_template
import folium

from agentes_quimicos import agentes_nao_persistentes, agentes_persistentes
from predicoes import (
    executar_predicao_simplificada,
    executar_predicao_nao_persistente,  # Corrigido
    executar_predicao_persistente,      # Corrigido
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Defaults (Rio de Janeiro)
    source_lat = -22.941
    source_lon = -43.1798
    wind_speed = 12.0   # km/h
    wind_direction = 90.0
    agente = ""
    meio = ""
    estabilidade = ""

    if request.method == "POST":
        try:
            source_lat = float(request.form.get("lat", source_lat))
            source_lon = float(request.form.get("lon", source_lon))
            wind_speed = float(request.form.get("wind_speed", wind_speed))
            wind_direction = float(request.form.get("wind_direction", wind_direction))
            agente = (request.form.get("agente") or "").strip().lower()
            meio = (request.form.get("meio") or "").strip().lower()
            estabilidade = (request.form.get("estabilidade") or "").strip().lower()
        except Exception:
            pass

    source = (source_lat, source_lon)
    map_obj = folium.Map(location=source, zoom_start=12)

    # Decide a predição
    if agente in agentes_nao_persistentes:
        executar_predicao_nao_persistente(   # Corrigido
            map_obj=map_obj,
            source=source,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            meio_de_lancamento=meio or "granada",
        )
    elif agente in agentes_persistentes:
        executar_predicao_persistente(   # Corrigido
            map_obj=map_obj,
            source=source,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            meio_de_lancamento=meio or "bomba",
        )
    else:
        executar_predicao_simplificada(
            map_obj=map_obj,
            source=source,
            wind_speed=wind_speed,
            wind_direction=wind_direction
        )

    # HTML do mapa (inclui Leaflet via CDN)
    map_html = map_obj._repr_html_()
    return render_template(
        "index.html",
        map_html=map_html,
        lat=source_lat,
        lon=source_lon,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        agente=agente,
        meio=meio,
        estabilidade=estabilidade
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=True)  # <--- debug ativado

