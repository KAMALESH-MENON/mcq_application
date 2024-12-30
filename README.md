# Pokemon API README

An API using Flask and the OpenAPI specification

## How to run (using terminal/command line)
From the root directory of the project, create a Python virtual environment with:

`python3 -m venv venv`

Then activate it. On Windows, use:

`.venv/bin/activate`

Once active, install the requirements with:

`pip install -r requirements.txt`

### Running migrations
Use `alembic` to update your local DB with

`alembic upgrade head`

### Run

Finally, run the application with:

`python -m uvicorn src.server:app --reload`

## Set up pre-commit hooks for linting
```
pip install pre-commit
pre-commit install
```

```shell
python -m pytest ./tests/unit/
```

```shell
python -m pytest ./tests/integration/
```

## Routes available:
- to be implemented
