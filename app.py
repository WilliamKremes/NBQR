from flask import Flask, request, render_template
import folium
from agentes_quimicos import agentes_nao_persistentes, agentes_persistentes
from predicoes import (
    executar_predicao_simplificada,
    executar_predicao_nao_persistente,
    executar_predicao_persistente,
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Valores padrão
    source_lat = -22.941
    source_lon = -43.1798
    wind_speed = 12.0
    wind_direction = 90.0
    agente = ""
    meio = "granada"
    estabilidade = "instável"

    if request.method == "POST":
        try:
            source_lat = float(request.form.get("lat", source_lat))
            source_lon = float(request.form.get("lon", source_lon))
            wind_speed = float(request.form.get("wind_speed", wind_speed))
            wind_direction = float(request.form.get("wind_direction", wind_direction))
            agente = (request.form.get("agente") or "").strip().lower()
            meio = (request.form.get("meio") or "granada").strip().lower()
            estabilidade = (request.form.get("estabilidade") or "instável").strip().lower()
        except Exception:
            pass

    source = (source_lat, source_lon)
    map_obj = folium.Map(location=source, zoom_start=12)

    # Decisão conforme tipo de agente químico
    if agente in agentes_nao_persistentes:
        executar_predicao_nao_persistente(
            map_obj, source, wind_speed, wind_direction,
            estabilidade_do_ar=estabilidade,
            meio_de_lancamento=meio
        )
    elif agente in agentes_persistentes:
        executar_predicao_persistente(
            map_obj, source, wind_speed, wind_direction,
            meio_de_lancamento=meio
        )
    else:
        executar_predicao_simplificada(map_obj, source, wind_speed, wind_direction)

    # Renderizar o mapa em HTML
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
    app.run(host="0.0.0.0", port=port)
