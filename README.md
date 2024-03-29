# BBQ-manager

BBQ manager is a tool for beauty saloon manager. It'll help to manage purchases and track used materials.

## Main task

In the end of the day manager should see how much money should saloon give to master's (or take from them). Also manager should see daily/monthly stats. See this [stats docs](./docs/stats.md) for more details.

## Run project locally

- Clone repository to your computer
- Change .env.dist to .env and fill it
- Make sure you have Docker and Docker Compose installed 
- Run project with `docker-compose up`
- On first run you need to apply migrations with `docker-compose exec web python manage.py migrate`
- Create superuser with `docker-compose exec web python manage.py createsuperuser`
- Collect static with `docker-compose exec web python manage.py collectstatic`
- Project is available at http://localhost:8000/

## Stack

- Python 3.9
- Django 4
- Django REST Framework
- Docker
- PostrgeSQL

## [![Repography logo](https://images.repography.com/logo.svg)](https://repography.com) / Top contributors
[![Top contributors](https://images.repography.com/28409406/Yakov-Varnaev/BBQ-manager/top-contributors/bd18c35f561de8a72274e2c10149ba50_table.svg)](https://github.com/Yakov-Varnaev/BBQ-manager/graphs/contributors)
