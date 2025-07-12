# Breaking down celery controller setup


```sh
docker run -it python:3.7.16-slim-buster bash
apt update
apt install git
git clone https://github.com/DDMAL/Rodan-lite

# Workdir /Rodan-lite

cd Rodan-lite
pip install -r requirements.txt
# ISSUES:
# - requirements.txt line 31: git+https://github.com/deepio/pybagit
# - "psycopg2==2.8.4" installation error
# - "uWSGI" package installation error

```