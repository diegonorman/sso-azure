#!/usr/bin/env bash
apt-get update && apt-get install -y libxml2-dev libxmlsec1-dev pkg-config xmlsec1
pip install -r requirements.txt
python manage.py migrate
