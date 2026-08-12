# Personal Finance App
## Description: 
A rest-API backend for managing Personal Finance. Built using python FastAPI and PostgreSQL via neon. Entirely developed using github's Codespace.

## Database Schema
For the ERD image, check file [Database ERD](Database%20ERD.png).
More explanation on database schema, check file [Database Schema](database.md).

## API documentation
https://anjelisa01.github.io/swagger-docs/

The server is NOT deployed because of technical issue, above link is a static page of the swagger UI for the API

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

## Tech Stacks
- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- JWT Authentication

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


