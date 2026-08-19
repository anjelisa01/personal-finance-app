# Personal Finance App
## Description: 
A rest-API backend for managing Personal Finance. Built using python FastAPI and PostgreSQL via neon. Entirely developed using github's Codespace.

## Overview
This is a personal project on FastAPI backend, i designed the database schema, the API, and the frontend (still unfinished).  
The project was built first with just one resource "user", after this user is connected and available then i add authentication, then i add more resources and revise and add more features as the project grow.  
I follow the clean architecture style so the project can be maintained and scale as needed.  

There's /frontend folder in the project's repo, which contains UI using streamlit, it's still unfinished and part of the further improvement of the application.  

For the testing, i did integration testing where i test the endpoints which including the services, the pydantic schemas, and sqlalchemy models (all have to be functional for the test to success). Currently i do not have unit testing.

I was planning to deployed via Railway but it required card information which i cannot provide, thus here i present my API using static page of my Swagger UI.

There's a lot to improve here to make the application smoother, safer and more robust.

## Database Schema
For the ERD image, check file [Database ERD](Database%20ERD.png).
More explanation on database schema, check file [Database Schema](database.md).

## API documentation
https://anjelisa01.github.io/swagger-docs/

The server is NOT deployed, above link is a static page of the swagger UI for the API

## Features:
- Secure user authentication with signup and login
- User profile management (view, update, and delete personal data)
- JWT-based authorization for protected API endpoints
- Financial resource management:
  - Accounts
  - Goals
  - Categories
  - Transactions
  - Budgets
- Full CRUD operations for all user-owned resources
- Protected routes accessible only to authenticated users
- Integration testing using Pytest

## Tech Stacks
- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- JWT Authentication
- Pytest

## Project Structure
``` 
PersonalFinanceApp/
|  backend/  
|     api/  
|     dependecies/  
|     core/  
|     models/  
|     schemas/  
|     services/  
|     tests/  
|     main.py  
```

## How to install
1. clone the repo
```
git clone <repository-url>
cd <project-directory>
```
2. create venv and activate
```
python -m venv .venv
source .venv/bin/activate
```
3. install dependencies
```
pip install -r requirements.txt
```
4. configure .env (copy .env.example then open .env and fill)
```
cp .env.example .env
```
5. run the server
```
uvicorn app.main:app --reload
```

## Future Improvement
- Deployment so it can be access live
- Add /dashboard endpoint
- Add Financial Goals Tracking feature