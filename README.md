# RentLyra API
RentLyra API is a ride sharing backend built with Django, PostgreSQL, and PostGIS.

## Prerequisites

- Python3.12 or above
- PostgresSQL database
- GeoSpatial Libraries ```sudo apt-get install binutils libproj-dev gdal-bin```
- If using the Nginx proxy then set ```client_max_body_size       100m;```
- Amazon Linux ```sudo amazon-linux-extras install postgresql14```
- Docker

## Database setup in Docker

```shell
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=postgres -d postgres:18
docker exec -it postgres bash
apt update
apt install postgis postgresql-18-postgis-3
su - postgres
```

OR use docker-compose from db/docker-compose.yml.sample

```commandline
docker-compose up -d
```

Create db user and password

```shell
psql
create database rent_lyra_db;
create user rent_lyra with encrypted password 'postgres';
grant all privileges on database rent_lyra_db to rent_lyra;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO rent_lyra;
exit
psql -d rent_lyra_db
CREATE EXTENSION postgis;
GRANT SELECT ON public._view TO rent_lyra;
alter table public._view owner to rent_lyra;
GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO rent_lyra;
```

## Project Setup

```shell
git clone https://github.com/jannatul29/RentLyra-Api.git
git checkout development
Copy `app.conf.sample` file from `core/config` directory and create `app.conf` in the same directory
Open file `core/config/app.conf` and put appropriates credentials
make virtualenv
source env/bin/activate
pip3 install uv
uv pip install -r requirements.txt
```

## Migrations

Django can create migrations for you. Make changes to your models - for example, adding a field and/or removing a
model - run
`makemigrations`:

```shell
python manage.py makemigrations
```

Once you have your new migration files, you should apply them to your database to make sure they work as expected:

```shell
python manage.py migrate db --database="default"
```

## Create Super User Once

```shell
python manage.py createsuperuser
```

Enter your desired username and press enter.

```text
Username: admin
```

You will then be prompted for your desired email address:

```text
Email address: admin@gmail.com
```

## Deployment

Run in local

```shell
python manage.py runserver
```

Run in Docker

```shell
docker build -t rent_lyra -f Dockerfile .
bash deploy.sh
```
