# Quizify

## Overview
Quizify is a user-friendly platform designed to streamline quiz management and user assessment. It offers a structured way for administrators to create quizzes while allowing users to participate, track their progress, and earn certificates.

## Purpose & Use Case
Quizify aims to simplify the process of quiz creation, administration, and participation. It serves both educators and learners by providing an easy-to-use platform for managing quizzes, tracking performance, and generating certificates for completed assessments.

## Problem It Solves
Traditional quiz management can be time-consuming and inefficient, especially when handling large question sets, tracking scores, and maintaining user records. Quizify solves this by:

- Enabling bulk MCQ uploads, reducing manual effort for quiz administrators.
- Implementing role-based access control to ensure secure and structured user management.
- Allowing users to attempt quizzes, track scores, and receive certificates for their submission.
- This application is ideal for educational institutions, corporate training programs, and any scenario requiring structured knowledge assessment.
## Roles
- **Admin**:
  - Bulk upload MCQs via an Excel file
  - Manage users (get, get_all, add, update, delete)
- **User**:
  - View available MCQ types (Python, Java, C#)
  - Select a category and attempt random MCQs
  - Submit responses and get a score and percentage
  - View their submission history
## Flow diagram
- **Admin**:
  - ![alt text](files/admin-flow.png)
- **User**:
  - ![alt text](files/user-flow.png)
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
    POST /api/v1/certificates/create - Generate Certificate for last submission of user.
    GET /api/v1/mcq/history - User Submission History
    GET /api/v1/mcq/history/{history_id} - User Submission History By ID
    GET /api/v1/mcq/history/{history_id}/certificate - Fetch certificate by history_id and generates presigned URL for certificate
 ### Admin Routes
    GET /api/v1/users - Get All Users
    POST /api/v1/users - Add User
    GET /api/v1/users/{user_id} - Get One User
    PATCH /api/v1/users/{user_id} - Update User
    DELETE /api/v1/users/{user_id} - Delete User
    POST /api/v1/bulk-upload - Bulk Upload MCQs
    POST /api/v1/mcq - Create MCQ
    POST /api/v1/upload-template - Upload Template


## User Interface Screenshots
  ### Login page
  ![Alt text](files/login.png)

  ### Register page
  ![Alt text](files/register.png)

  ### User Dashboard page
  ![Alt text](files/user-dashboard.png)

  ### User Quiz Attempt page
  ![Alt text](files/user-quiz-attempt.png)

  ### User Result after submission
  ![Alt text](files/results-after-submission.png)

  ### User Review submitted Quiz
  ![Alt text](files/submitted-review.png)

  ### User Submission history page
  ![Alt text](files/user-submit-history.png)

  ### Admin Quiz Management page
  ![Alt text](files/admin-features-1.png)

  ### Admin User Management page
  ![Alt text](files/admin-features-2.png)
  ![Alt text](files/admin-feature-add-user.png)
