from fastapi import FastAPI
from src.app.config.database import Base, engine
from src.app.models import data_models as models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
print("Tables created.")
