# Use a imagem base do Python
FROM python:3.9-slim

# Configuração do diretório de trabalho no container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY requirements.txt ./
COPY app.py ./
COPY templates ./templates
COPY scripts ./scripts

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta onde a aplicação Flask estará rodando
EXPOSE 5000

# Comando para executar a aplicação quando o contêiner for iniciado
CMD ["python", "app.py"]
