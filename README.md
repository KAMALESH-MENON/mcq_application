# Quizify

The MCQ Application API is a backend service built using FastAPI, SQLAlchemy, and PostgreSQL. It supports role-based access control with two roles: Admin and User. Admins can manage users and upload MCQs in bulk, while users can attempt quizzes and track scores and can generate certificate for their last submission.

## Roles & Permissions
- **Admin**:
  - Bulk upload MCQs via an Excel file
  - Manage users (get, get_all, add, update, delete)
- **User**:
  - View available MCQ types (Python, Java, C#)
  - Select a category and attempt random MCQs
  - Submit responses and get a score and percentage
  - View their submission history

## Tech Stack

    Backend: FastAPI (Python)
    Database: PostgreSQL with SQLAlchemy ORM
    Architecture: Repository Pattern, Service Layer & Unit of Work approach

## Installation
1. Clone the repository

    `git clone https://github.com/KAMALESH-MENON/mcq_application.git`

    `cd mcq_application`

2. From the root directory of the project, create a Python virtual environment with:

    `python3 -m venv venv`

3. Then activate it. On Windows, use:

    `. venv/Scripts/activate.bat`
    On Windows, use:

    `. venv/Scripts/activate.bat`

4. Once active, install the requirements using pipenv if it is already installed. Otherwise, first install pipenv by running `pip install pipenv`, then use the following command:

    `pipenv install -r requirements.txt`

5. Create a .env (or rename the .env.example to .env) file with the following variables:

    ```
    CONNECTION_URL = "postgresql+psycopg2://your_username:your_password@your_host:your_port/your_database_name"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    SECRET_KEY = "your_actual_secret_key"
    ```

### Running migrations
Use `alembic` to update your local DB with

`alembic upgrade head`

### Run the application
Change directory to src

`cd src`

Finally, run the application with:

`uvicorn server:app --reload`

## Set up pre-commit hooks for linting
```
pip install pre-commit
pre-commit install
```
## Architecture Diagram
![Alt text](files/architecture-diagram.png)

## API Endpoints
 ### Authentication
    POST /api/v1/auth/register - Register
    POST /api/v1/auth/login - Login
    GET /api/v1/auth/me - Get Current User
    POST /api/v1/auth/refresh - Refresh Token
 ### MCQ Routes
    GET /api/v1/mcq/types - Get MCQ Types
    GET /api/v1/mcq/ - Get Random MCQs
    POST /api/v1/mcq/submit - Submit Answers
    POST /api/v1/certificates/create - Generate Certificate
    GET /api/v1/mcq/history - User Submission History
    GET /api/v1/mcq/history/{history_id} - User Submission History By ID
 ### Admin Routes
    GET /api/v1/users - Get All Users
    POST /api/v1/users - Add User
    GET /api/v1/users/{user_id} - Get One User
    PATCH /api/v1/users/{user_id} - Update User
    DELETE /api/v1/users/{user_id} - Delete User
    POST /api/v1/bulk-upload - Bulk Upload MCQs
    POST /api/v1/mcq - Create MCQ
    POST /api/v1/upload-template - Upload Template
