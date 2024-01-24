# Stock Trading App

## Overview

The Stock Trading App is a Django-based web application that allows users to register, manage stock data, and perform transactions. This document provides an overview of the project structure, setup instructions, and details about the implemented endpoints.

## Project Structure

- **stockTrading:** Django project root directory.
- **stockTradingApp:** Django app containing models, views, serializers, and other components.
- **celery.py:** Configuration file for Celery tasks.
- **tasks.py:** Defines Celery tasks for asynchronous processing.

## Setup Guide

### 1. Prerequisites

Ensure you have the following installed on your system:

- Python
- Django
- PostgreSQL
- Redis
- Celery
- Swagger
- Docker

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Environment varibale

```bash
SECRET_KEY=""
DATABASE_NAME=""
DATABASE_USER=""
DATABASE_PASSWORD=""
DATABASE_HOST=""
DATABASE_PORT=""
REDIS_URL=""
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Celery

```bash
celery -A stockTrading worker -l info
```

### 6. Run Django Development Server

```bash
python manage.py runserver
```

### 7. End Points

* **Users:**
    * `POST /users/`: Register a new user.
    * `GET /users/{username}/`: Retrieve user data.
* **Stocks:**
    * `POST /stocks/`: Ingest stock data.
    * `GET /stocks/list/`: Retrieve all stock data.
    * `GET /stocks/{ticker}/`: Retrieve specific stock data.
* **Transactions:**
    * `POST /transactions/`: Post a new transaction.
    * `GET /transactions/{user_id}/`: Retrieve all transactions of a specific user.
    * `GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/`: Retrieve transactions between two timestamps.

### 7.i. End Points Schema
* **To view the schema of all the end pints schema goto the follwoing url after running**
* `/api_schema`

### 8. Swagger Documentation
* **For Swagger Documentation goto the following url after running**
* `docs/`

### 9. Flower Dashboard for monitoring celery

```bash
celery -A stockTrading flower
```

### 10. Unit Testing

```bash
python manage.py test
```

## For Running in Docker
* **apply the follwong commands in order**
* Build and run docker:
```bash
docker-compose build
docker-compose up
```

* For access logs of the container
```bash
docker-compose logs web
```

* For Clean Up
```bash
docker-compose down
```


## Assumptions:
* **Already Installed**
* Python 
* pip
* Django
* Docker 