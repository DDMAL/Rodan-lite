# Breaking down celery controller setup


```sh
docker run -it python:3.7.16-slim-buster bash
apt update
apt install -y \
    build-essential \
    git \
    libpq-dev
git clone https://github.com/DDMAL/Rodan-lite

# Workdir /Rodan-lite

cd Rodan-lite
pip install -r requirements.txt
# ISSUES:
# - requirements.txt line 31: git+https://github.com/deepio/pybagit
pip install poetry==1.4.2
pip install setuptools==58
poetry install
# ISSUES:
# - anyjson. I noticed no code is using this, and python3 has built-in `json`
# Solution: Remove poetry.lock and install dependencies again
# -----------
# New dependencies (remaking pyproject.toml)
# Django: 3.2
# Celery: 5.2
```