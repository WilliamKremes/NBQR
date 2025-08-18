# NBQR Top (Flask + Folium)

App web simples para gerar mapas de predição NBQR com **Folium**. Pronto para deploy no **Render**.

## Rodar localmente
```bash
pip install -r requirements.txt
python app.py
# abra http://localhost:10000
```

## Deploy no Render
- Faça push deste projeto para um repositório (GitHub/GitLab/Bitbucket).
- No Render: **New → Web Service** → conecte o repo.
- O Render usa `render.yaml`:
  - build: `pip install -r requirements.txt`
  - start: `gunicorn app:app --bind 0.0.0.0:$PORT`

## Como usar
- Preencha latitude/longitude, vento (km/h), direção (°).
- Informe **agente**:
  - Se vazio → *predição simplificada*.
  - Se for **não persistente** → usa estabilidade do ar (instável/neutra/estável).
  - Se for **persistente** → usa *meio de lançamento* (bomba, granada, espargimento…).
