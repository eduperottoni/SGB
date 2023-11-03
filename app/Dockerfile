FROM python:3.11-alpine

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de requirements (se existir) para o contêiner
COPY src/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte da aplicação para o contêiner
COPY src/ /app

# Define a porta que a aplicação irá expor
EXPOSE 8080

# Comando para executar a aplicação Flask
CMD ["python", "app.py"]

