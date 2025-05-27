FROM python:3.11-slim

# Instala dependências de sistema necessárias para o SAML
RUN apt-get update && \
    apt-get install -y libxml2-dev libxmlsec1-dev pkg-config xmlsec1 gcc g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Executa migrações e coleta arquivos estáticos antes de iniciar o servidor
CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn semeq_sso.wsgi:application --bind 0.0.0.0:8000
