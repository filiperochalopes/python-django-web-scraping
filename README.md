```sh
docker-compose build --no-cache
docker-compose up -d
firefox localhost:8089/docs
```

### Realizando dump de banco de dados

```sh
# backup sqlite3
sqlite3 db.sqlite3 .dump > dump.sql
# restore sqlite3
mv db.sqlite3 _db.sqlite3
sqlite3 db.sqlite3 < dump.sql
```

### Inicializando migrações

```sh
docker exec -it samuel_webscraping_djangoapp bash -c "cd /usr/src/app/app && python manage.py makemigrations"
docker exec -it samuel_webscraping_djangoapp bash -c "cd /usr/src/app/app && python manage.py migrate"
```

### Coletando arquivos estáticos

Necessário para capturar arquivos para criar pdf

```sh
docker exec -it samuel_webscraping_djangoapp bash -c "cd /usr/src/app/app && python manage.py collectstatic"
```

## Realizando deploy

Defina as variáveis de ambiente utilizadas na aplicação

```sh
cp .env.example .env
```

Suba os containers docker

```sh
docker-compose up -d
```

Rode as migrações necessárias para a aplicação completa django para evitar warnings

```sh
docker exec -it samuel_webscraping_djangoapp bash -c "cd /usr/src/app/app && python manage.py migrate"
```
