# AniRec+ (Backend)
Here is the link to front-end repository: [Anirec-Frontend](https://github.com/shaikhdanialsah/Anirec-Frontend)

<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />&nbsp;
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />&nbsp;
<img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit learn&logoColor=white" />&nbsp;
<img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white" />&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white" />

## Overview

This is the backend for an anime recommendation system built using **Flask** and connected to a **PostgreSQL** database (Supabase) and  hosted on **Koyeb**. The system includes an API that allows users to query anime recommendations based on their input (e.g., anime title), along with additional functionalities like user authentication (sign-up/login).

## Features

- **Anime Recommendations**: Users can input an anime title, and the system will return a list of recommended animes based on a content-based filtering method using NLP (TF-IDF and Cosine Similarity).
- **User Authentication**: Allows users to sign up and log in to access personalized recommendations and view history.
- **PostgreSQL Integration**: Stores user data and anime information in a PostgreSQL database hosted on Koyeb.
- **API Endpoints**: Exposes RESTful APIs for interacting with the system.

## Technologies Used

- **[Flask](https://flask.palletsprojects.com/en/stable/)**: Web framework for building the API.
- **[PostgreSQL](https://www.postgresql.org/)**: Relational database to store anime details and user information.
- **[SupaBase](https://supabase.com/)**: Cloud PostgreSQL database
- **[JSON Web Tokens (JWT)](https://jwt.io/0)**: For user authentication.
- **TF-IDF & Cosine Similarity**: Used for content-based filtering to recommend anime based on descriptions.
- **[Koyeb](https://www.koyeb.com/)**: Hosting platform for the backend.

## Installation

To run the backend locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/shaikhdanialsah/Anime-Backend.git
cd Anime-Backend
```
### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup the database and JSON Web Tokens
Ensure that you have a PostgreSQL databases locally or on any hosted database platforms such as Koyeb or SupaBase and add the credentials to your `.env` file
```bash
DATABASE_NAME='YOUR_DATABASE_NAME'
DATABASE_USER='YOUR_DATABASE_USERNAME'
DATABASE_PASSWORD='YOUR_DATABASE_PASSWORD'
DATABASE_HOST='YOUR_DATABASE_HOSTNAME'
JWT_SECURE_KEY='YOUR_JWT_SECURE_KEY'
```
It is best for the JWT secure key to be long `(up to 32 characters)` and completely random. Here's how to generate a random JWT secure key with python

```python
import secrets
print(secrets.token_hex(32)) 
```

### 5. Run the Flask app
```bash
python app.py
```
The backend will be running on `http://localhost:5000`.

## API Endpoints (Example)

### 1. `/api/recommend?anime=anime_name` (POST)

- Description: Returns anime recommendations based on the `input anime title`.
  Example usage:
  ```bash
  /api/recommend?anime=Naruto
  ```
### 2. `/api/signup` (POST)
- Description: Returns data for `user signup`

### 3. `/api/login` (POST)
- Description: Returns data for `use login` in form of JWT token.

##  Running in Production
To deploy the backend to Koyeb, follow these steps:

1. Set up the app on Koyeb and connect to your `PostgreSQL database`.
2. Push the app to Koyeb using Git or other deployment methods.
3. Make sure the environment variables (like `DATABASE_NAME, DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USER`) are properly configured.
4. Add a Procfile file so Koyeb knows how to start your application.
```bash
gunicorn module_name:application_instance_name
``` 

## License
This project is licensed under the MIT License - see the [MIT](https://choosealicense.com/licenses/mit/) file for details.
