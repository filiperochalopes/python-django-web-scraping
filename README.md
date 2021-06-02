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


Primeiro suba o container

```sh
docker-compose up -d
```

Rode as migrações necessárias para a aplicação completa django para evitar warnings

```sh
docker exec -it samuel_webscraping_djangoapp bash -c "cd /usr/src/app/app && python manage.py migrate"
```
