from flask import Flask, request, render_template
import folium
from agentes_quimicos import agentes_nao_persistentes, agentes_persistentes
from predicoes import (
    executar_predicao_simplificada,
    executar_predicao_nao_persistente,
    executar_predicao_persistente,
)

app = Flask(__name__)  # <- ESSENCIAL

@app.route("/", methods=["GET", "POST"])
def index():
    # Valores padrão
    source_lat = -22.941
    source_lon = -43.1798
    wind_speed = 12
    wind_direction = 90
    agente = ""
    meio = ""
    estabilidade = ""
    source_final = None  # Inicializa source_final

    if request.method == "POST":
        try:
            source_lat = float(request.form.get("lat", source_lat))
            source_lon = float(request.form.get("lon", source_lon))
            wind_speed = float(request.form.get("wind_speed", wind_speed))
            wind_direction = float(request.form.get("wind_direction", wind_direction))
            agente = (request.form.get("agente") or "").strip().lower()
            meio = (request.form.get("meio") or "granada").strip().lower()
            estabilidade = (request.form.get("estabilidade") or "instável").strip().lower()

            lat_final = request.form.get("lat_final")
            lon_final = request.form.get("lon_final")
            if lat_final and lon_final:
                source_final = (float(lat_final), float(lon_final))
        except Exception:
            pass

    source = (source_lat, source_lon)
    map_obj = folium.Map(location=source, zoom_start=12)

    if agente in agentes_nao_persistentes:
        executar_predicao_nao_persistente(
            map_obj, source, wind_speed, wind_direction,
            estabilidade_do_ar=estabilidade,
            meio_de_lancamento=meio
        )
    elif agente in agentes_persistentes:
        if meio in ["espargimento", "gerador"] and source_final is None:
            raise ValueError("Para meios de lançamento 'espargimento' ou 'gerador', 'source_final' deve ser informado.")
        executar_predicao_persistente(
            map_obj,
            source,
            wind_speed,
            wind_direction,
            meio_de_lancamento=meio,
            source_final=source_final
        )
    else:
        executar_predicao_simplificada(map_obj, source, wind_speed, wind_direction)

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
        estabilidade=estabilidade,
        lat_final=source_final[0] if source_final else "",
        lon_final=source_final[1] if source_final else ""
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
