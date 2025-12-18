# Dockerfile
FROM python:3.12-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia o requirements primeiro (cache eficiente)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app ./app

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando padrão para rodar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
