# QRkot_spreadseets
Учебный проект. API приложения для Благотворительного фонда поддержки котиков QRKot. 
Его назначение — сбор и распределение пожертвований между различными проектами и формирование отчетов о времени закрытия проектов
в гугл таблицах

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [REST API](#rest-api)
- [Над проектом работали](#над-проектом-работали)

## Технологии
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](http://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
- [Google Cloud Platform](https://cloud.google.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Drive API](https://developers.google.com/drive)
- [Uvicorn](https://www.uvicorn.org/)

## Использование
Склонируйте репозиторий  
Создайте виртуальное окружение 
```
python -m venv venv
```
Активируйте виртуальное окружение  
Установите зависимости 
```
pip install -r requirements.txt
```
Отредактируйте и переименуйте  `.env.template`. в  `.env`  
Примените миграции
```
alembic upgrade head
```
Запустите сервер из корневой папки проекта
```
uvicorn app.main:app --reload
```
При первом запуске приложения будет создан суперюзер, с регистрационными данными из `.env`  

## REST API
Документация и web интервейс API будет доступен по адресу: http://localhost:8000/docs

## Над проектом работали
- [Алексей Туктанов](https://t.me/atuktanov)
