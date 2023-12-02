import json
import re
import pandas as pd
import pymongo

caminho_arquivo_excel = '/Users/lbayout/PycharmProjects/pythonProject13/xcell_files/fileoutpart0.xlsx'
dados_excel = pd.read_excel(caminho_arquivo_excel)

# client = pymongo.MongoClient("mongodb+srv://lucas:bayout@cluster0.uqxmkzv.mongodb.net/?retryWrites=true&w=majority")
# db = client["dados_trading"]
# collection = db["dados_por_dia"]

def preco_e_ajuste():
    dados_coluna_e = dados_excel.iloc[1:, 4]
    valores_numericos = [re.sub(r'[^0-9,.]', '', str(valor)) for valor in dados_coluna_e]
    valores_monetarios = []

    for valor in valores_numericos[2:]:
        if re.match(r'^\d{1,3}(?:\.\d{3})*(?:,\d+)?$', valor):
            valores_monetarios.append(valor)

    return valores_monetarios

def vencimento():
    dados_coluna_b = dados_excel.iloc[1:, 1]
    datas_formato_valido = []
    for valor in dados_coluna_b:
        match = re.search(r'(\d{2}/\d{2}/\d{4})', str(valor))
        if match:
            datas_formato_valido.append(match.group(1))
    return datas_formato_valido

def nome_e_tipo_de_acao_diaria():
    dados_coluna_a = dados_excel.iloc[1:, 0]
    padrao = re.compile(r'[CV]\s[A-Z0-9]+\b')
    valores_filtrados = [
        re.sub(r'\s_x000D_$', '', valor.split('_x000D_')[0]) for valor in dados_coluna_a
        if padrao.search(str(valor)) and not valor.endswith('_x000D_[_J _x000D_I Venda disponfvel')
    ]
    tuplas_acao = []
    for valor in valores_filtrados:
        partes = valor.split()
        if len(partes) == 2:
            tuplas_acao.append((partes[0].strip(), partes[1].strip()))
    return tuplas_acao

def quantidade():
    dados_coluna_d = dados_excel.iloc[1:, 3]
    quantidades = []
    for valor in dados_coluna_d:
        match = re.findall(r'\d+,\d+', str(valor))  # Procura por números no formato XX,XX
        if match:
            quantidades.extend(match)

    return quantidades

def valor_da_operacao_preco_ajuste():
    dados_coluna_h = dados_excel.iloc[1:, 7]  # Considerando a coluna H como índice 7
    valores_numericos = [re.sub(r'[^0-9,.]', '', str(valor)) for valor in dados_coluna_h]
    valores_monetarios = []

    for valor in valores_numericos:
        if re.match(r'^\d{1,3}(?:\.\d{3})*(?:,\d+)?$', valor):
            valores_monetarios.append(valor)

    return valores_monetarios

def total_liquido_nota():
    valor_total = dados_excel.iloc[35, 9]  # Lembre-se que a indexação começa em 0, então é [35, 9] para a linha 36, coluna J
    valor_total = re.sub(r'[^0-9,.]', '', str(valor_total))
    valor_numerico = float(valor_total.replace(',', '.'))  # Converte para um número decimal
    return valor_numerico

def total_despesas_nota():
    valor_total = dados_excel.iloc[34, 9]  # Lembre-se que a indexação começa em 0, então é [35, 9] para a linha 36, coluna J
    valor_total = re.sub(r'[^0-9,.]', '', str(valor_total))
    valor_numerico = float(valor_total.replace(',', '.'))  # Converte para um número decimal
    return valor_numerico

def total_liquido():
    valor_total = dados_excel.iloc[35, 7]  # Lembre-se que a indexação começa em 0, então é [35, 9] para a linha 36, coluna J
    valor_total = re.sub(r'[^0-9,.]', '', str(valor_total))
    valor_numerico = float(valor_total.replace(',', '.'))  # Converte para um número decimal
    return valor_numerico

def total_valor_negocios():
    valor_total = dados_excel.iloc[34, 7]  # Lembre-se que a indexação começa em 0, então é [35, 9] para a linha 36, coluna J
    valor_total = re.sub(r'[^0-9,.]', '', str(valor_total))
    valor_numerico = float(valor_total.replace(',', '.'))  # Converte para um número decimal
    return valor_numerico

preco_ajuste = preco_e_ajuste()
vencimentos = vencimento()
nome_tipo_acao = nome_e_tipo_de_acao_diaria()
quantidades = quantidade()
valores_operacao_preco_ajuste = valor_da_operacao_preco_ajuste()
total_liquido_nota_val = total_liquido_nota()
total_despesas_nota_val = total_despesas_nota()
total_liquido_val = total_liquido()
total_valor_negocios_val = total_valor_negocios()

resultados = {
    "preco_e_ajuste": preco_e_ajuste(),
    "vencimento": vencimento(),
    "nome_e_tipo_de_acao_diaria": nome_e_tipo_de_acao_diaria(),
    "quantidade": quantidade(),
    "valor_da_operacao_preco_ajuste": valor_da_operacao_preco_ajuste(),
}

dados_por_dia = {f'dia_{i+1}': {} for i in range(30)}

for chave, lista in resultados.items():
    for i in range(30):
        dados_por_dia[f'dia_{i+1}'][chave] = lista[i::30]

