#!/usr/bin/env bash
# Instala dependências de sistema necessárias para o SAML
apt-get update && apt-get install -y libxml2-dev libxmlsec1-dev pkg-config xmlsec1
# Instala dependências Python
pip install --upgrade pip
pip install -r requirements.txt
# Aplica as migrações do Django
python manage.py migrate
