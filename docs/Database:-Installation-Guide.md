# Rodan Database Manual Installation Guide

> Courtesy of ChatGPT

Here is the updated version with **code blocks** for each bullet point:

---

## 🔧 PostgreSQL Setup

### 1. Install PostgreSQL

```sh
sudo apt-get install postgresql postgresql-contrib postgresql-plpython
```

### 2. Start PostgreSQL

```sh
sudo -i -u postgres
psql postgres
```

### 3. Create Database & User *(in psql shell)*

```sh
# psql_shell
create user $DB_USER with password '$DB_PASSWORD';
alter user $DB_USER with createdb;
create database $DB_NAME;
grant all privileges on database "$DB_NAME" to $DB_USER;
```

### 4. Enable Remote Access

- Edit `/etc/postgresql/9.3/main/postgresql.conf`:
```sh
listen_addresses = '*'
```

- Edit `/etc/postgresql/9.3/main/pg_hba.conf`:
```
host  $DB_NAME  $DB_USER  $SUBNET  md5
```

### 5. Restart PostgreSQL

```sh
sudo /etc/init.d/postgresql reload
sudo /etc/init.d/postgresql restart
```

---

## 🌐 WebSocket Messaging Support (Redis + Superuser)

### 1. Install Redis & Python Packages

```sh
sudo apt-get install redis-server
sudo pip install psycopg2 redis
```

### 2. Create PostgreSQL Superuser *(in psql shell)*

```sh
create user $DB_SU_USER with password '$DB_SU_PASSWORD';
alter user $DB_SU_USER with superuser;
```

### 3. Allow Superuser Access

Edit `/etc/postgresql/9.3/main/pg_hba.conf`:

```conf
host  $DB_NAME  $DB_SU_USER  $RODAN_SERVER_IP/32  md5
```

### 4. Restart PostgreSQL

```sh
sudo /etc/init.d/postgresql reload
sudo /etc/init.d/postgresql restart
```
