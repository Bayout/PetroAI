import json
import statistics
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

from werkzeug import Response

from scripts.xcell_to_json import preco_e_ajuste, vencimento, nome_e_tipo_de_acao_diaria, quantidade, \
    valor_da_operacao_preco_ajuste, total_liquido_nota, total_despesas_nota, total_liquido, total_valor_negocios
from API_adobe.src.extractpdf.extract_txt_table_info_from_pdf import extract_pdf

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
EXCEL_FOLDER = 'excel_files'
JSON_FOLDER = 'json_files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXCEL_FOLDER'] = EXCEL_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file() -> Response:
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'Nenhum arquivo encontrado'
        # Get the file from post request
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file.filename == '':
            return 'Nenhum arquivo selecionado'

        # Save the file in the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract the data from the file
        file_path = os.path.join(app.config['EXCEL_FOLDER'], file.filename)
        extract_pdf()
        return redirect(url_for('display_metrics'))


@app.route('/metrics')
def display_metrics():
    file_path = os.path.join(app.config['JSON_FOLDER'], 'dados_mensal_day_trade.json')
    with open(file_path, 'r') as file:
        data = json.load(file)

    nome_e_tipo_acao = [item[1] for dia in data.values() for item in dia['nome_e_tipo_de_acao_diaria']]
    precos = [float(p.replace(',', '.')) for dia in data.values() for p in dia['preco_e_ajuste']]
    diferenca = precos[-1] - precos[0]
    media_precos = sum(precos) / len(precos)
    preco_maximo = max(precos)
    preco_minimo = min(precos)
    variacao_percentual = ((precos[-1] - precos[0]) / precos[0]) * 100
    desvio_padrao = statistics.stdev(precos)

    metrics_data = {
        'nome_e_tipo_acao': nome_e_tipo_acao,
        'diferenca': diferenca,
        'media_precos': media_precos,
        'preco_maximo': preco_maximo,
        'preco_minimo': preco_minimo,
        'variacao_percentual': variacao_percentual,
        'desvio_padrao': desvio_padrao,
    }

    return render_template('metrics.html', metrics_data=metrics_data)


if __name__ == '__main__':
    app.run(debug=True)
