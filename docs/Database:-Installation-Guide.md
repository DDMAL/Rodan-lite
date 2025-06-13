# Rodan Database Installation Guide
> Courtesy of ChatGPT

## 🔧 PostgreSQL Setup

| **Step** | **Ubuntu** | **macOS** |
|---------|------------|-----------|
| **1. Install PostgreSQL** | `sudo apt-get install postgresql postgresql-contrib postgresql-plpython` | `brew install postgresql`<br>`brew install postgres --with-python` |
| **2. Start PostgreSQL** | `sudo -i -u postgres`<br>`psql postgres` | `postgres -D /usr/local/var/postgres`<br>`brew services start postgresql`<br>`psql postgres` |
| **3. Create Database & User** *(in psql shell)* | - `create user $DB_USER with password '$DB_PASSWORD';`<br>- `alter user $DB_USER with createdb;`<br>- `create database $DB_NAME;`<br>- `grant all privileges on database "$DB_NAME" to $DB_USER;` | Same as Ubuntu |
| **4. Enable Remote Access** | Edit `/etc/postgresql/9.3/main/postgresql.conf`:<br>`listen_addresses = '*'`<br><br>Edit `/etc/postgresql/9.3/main/pg_hba.conf`:<br>`host  $DB_NAME  $DB_USER  $SUBNET  md5` | Config file may be at:<br>`/usr/local/var/postgres/pg_hba.conf` |
| **5. Restart PostgreSQL** | `sudo /etc/init.d/postgresql reload`<br>`sudo /etc/init.d/postgresql restart` | `brew services restart postgres` |

---

## 🌐 WebSocket Messaging Support (Redis + Superuser)

| **Step** | **Ubuntu** | **macOS** |
|---------|------------|-----------|
| **1. Install Redis & Python Packages** | `sudo apt-get install redis-server`<br>`sudo pip install psycopg2 redis` | `brew install redis`<br>`sudo pip install psycopg2 redis` |
| **2. Create PostgreSQL Superuser** *(in psql shell)* | `create user $DB_SU_USER with password '$DB_SU_PASSWORD';`<br>`alter user $DB_SU_USER with superuser;` | Same as Ubuntu |
| **3. Allow Superuser Access** | Edit `/etc/postgresql/9.3/main/pg_hba.conf`:<br>`host  $DB_NAME  $DB_SU_USER  $RODAN_SERVER_IP/32  md5` | Config file may be at:<br>`/usr/local/var/postgres/pg_hba.conf` |
| **4. Restart PostgreSQL** | `sudo /etc/init.d/postgresql reload`<br>`sudo /etc/init.d/postgresql restart` | `brew services restart postgres` |
