# Rodan Worker Setup Guide

> Courtesy of ChatGPT

This document focuses on setting up the **Rodan worker** manually (pre-Docker days).

---

## 📁 Clone Rodan Source Code

Ensure you perform a **recursive clone** to include submodules:

```bash
git clone --recursive https://github.com/DDMAL/Rodan.git
```

Set an environment variable for the project root:

```bash
export RODAN_HOME=/absolute/path/to/Rodan
cd $RODAN_HOME
```

---

## 🐍 Python Environment Setup

Rodan uses **Python 2.7.x**. Python 3 is **not supported**.

### 1. Install Virtualenv

```bash
sudo pip install virtualenv
```

### 2. Create Virtual Environment

```bash
cd $RODAN_HOME
virtualenv --no-site-packages rodan_env
source rodan_env/bin/activate
```

Your prompt should now look like:

```bash
(rodan_env)$
```

To deactivate the environment later, use:

```bash
deactivate
```

---

### 3. Install System Libraries (Ubuntu)

```bash
sudo apt-get install libpython-dev lib32ncurses5-dev:i386 libxml2-dev \
libxslt1-dev zlib1g-dev lib32z1-dev libjpeg-dev libpq-dev
```

> 💡 If `lib32z1-dev` fails, download it from [packages.ubuntu.com](https://packages.ubuntu.com/trusty/i386/libbz2-dev/download)

Install helper tools if issues persist:

```bash
sudo apt-get install aptitude
sudo apt-get -f install
```

---

### 4. Install Python Packages

```bash
pip install -r requirements.txt
pip install Werkzeug
```

---

### 5. Platform-Specific Notes

- **macOS**:

  - Set compiler: `export CC=gcc`
  - Use `gnureadline` instead of `readline`: [gnureadline PyPI](https://pypi.org/project/gnureadline/)

- **uWSGI Issue**:
  - If you see: `error: use of undeclared identifier 'SOL_TCP'`
  - Update `requirements.txt`:  
    Change `uWSGI==2.0.11.1` → `uWSGI==2.0.15`

---

## 📦 Optional: Install NFS Client (Linux only)

```bash
sudo apt-get install nfs-common inotify-tools
```

Create a mount directory for your NFS resource folder.

---

## ⚙️ Configure Rodan

### 1. Generate `SECRET_KEY`

```python
import random, string
print('SECRET_KEY={0}'.format(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(40))))
```

### 2. Run `autoconf` and configure Rodan

Install `autoconf`:

- **Ubuntu**: `sudo apt-get install autoconf`
- **macOS**: `brew install autoconf`

Run configuration (replace paths and values accordingly):

```bash
autoconf
./configure --enable-debug=no --enable-diva MODE="worker" \
  RODAN_VENV_DIR=$RODAN_HOME/rodan_env \
  RODAN_DATA_DIR=$RODAN_HOME/data \
  AMQP_HOST="localhost" AMQP_PORT="5672" AMQP_VHOST="rodan" \
  AMQP_USER="rodan" AMQP_PASSWORD="12345" \
  DB_HOST="localhost" DB_PORT="5432" \
  DB_NAME="rodan" DB_USER="rodan" DB_PASSWORD="12345" \
  DB_REDIS_PORT="6379" DB_REDIS_DBNUMBER=0 \
  WWW_USER="www-data" WWW_GROUP="www-data" \
  SECRET_KEY="YOUR_SECRET_KEY_HERE" \
  --with-graphicsmagick-search-path="/myhome/bin/" \
  --with-kdu_compress-search-path="/myhome/bin/" \
  --with-xmllint-search-path="/myhome/bin/" \
  --with-vips-search-path="/myhome/bin/"
```

Update file permissions (if prompted):

```bash
sudo chgrp -R www-data $RODAN_HOME/*
sudo chown www-data:www-data $RESOURCE_FOLDER_MOUNT_POINT
```

Update `settings.py`:

- Replace `@EMAIL_USERNAME@` and `@EMAIL_PASSWORD@` with actual credentials or empty strings.
- Replace `@MAX_PAGINATE_BY@` with `100`.

---

## 🖥️ Continue Setup

- Follow the **Rodan Web Server** guide (skip the `configure` step).
- Proceed with the **Rodan Client** installation to enable the UI.

---

## 🛠 Optional: Run with Supervisor

Install [Supervisor](http://supervisord.org/):

```bash
# Ubuntu
sudo apt-get install supervisor

# macOS
brew install supervisor
```

Copy the generated config:

```bash
cp $RODAN_HOME/etc/supervisor/conf.d/rodan.conf /etc/supervisor/conf.d/
```

---

## 🖼 Optional: Set Up Image Processing Jobs

See [Rodan Documentation](https://github.com/DDMAL/Rodan/wiki) for instructions on enabling optical music recognition (OMR) and image processing tasks.
