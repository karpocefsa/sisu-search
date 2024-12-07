
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Carregar dados do CSV
DATA_PATH = 'MICRODADOS_ED_SUP_IES_2023.CSV'
data = pd.read_csv(DATA_PATH, sep=';', encoding='latin-1')

@app.route('/')
def index():
    estados = data['SG_UF_IES'].dropna().unique()
    municipios = data['NO_MUNICIPIO_IES'].dropna().unique()
    return render_template('index.html', estados=sorted(estados), municipios=sorted(municipios))

@app.route('/resultados', methods=['POST'])
def resultados():
    estado = request.form.get('estado')
    municipio = request.form.get('municipio')

    resultados = data
    if estado:
        resultados = resultados[resultados['SG_UF_IES'] == estado]
    if municipio:
        resultados = resultados[resultados['NO_MUNICIPIO_IES'] == municipio]

    # Exibir apenas as colunas NO_IES e NO_BAIRRO_IES com os títulos 'Nome' e 'Bairro'
    resultados = resultados[['NO_IES', 'NO_BAIRRO_IES']].rename(
        columns={'NO_IES': 'Nome', 'NO_BAIRRO_IES': 'Bairro'}
    )

    return render_template('resultados.html', tabelas=resultados.to_html(classes='table table-striped', index=False))

if __name__ == '__main__':
    app.run(debug=True)
