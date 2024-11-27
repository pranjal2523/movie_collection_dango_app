# Movie Collection Management System

## Overview
A Django-based web application for managing movie collections with external movie API integration, user authentication, and request tracking.

## Features
- User registration with JWT authentication
- Movie listing from external API
- Create, read, update, and delete movie collections
- Top genre tracking
- Request counting middleware

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/pranjal2523/movie_collection_dango_app
cd movie_collection_dango_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```
DJANGO_SECRET_KEY=your_secret_key
MOVIE_API_USERNAME=your_api_username
MOVIE_API_PASSWORD=your_api_password
DEBUG=False
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /register/`: User registration

### Movies
- `GET /movies/`: List movies (paginated)

### Collections
- `GET /collection/`: List user collections
- `POST /collection/`: Create collection
- `GET /collection/<uuid>/`: Retrieve specific collection
- `PUT /collection/<uuid>/`: Update collection
- `DELETE /collection/<uuid>/`: Delete collection

### Monitoring
- `GET /request-count/`: Get total request count
- `POST /request-count/reset/`: Reset request counter

