import pytest
from sqlalchemy.orm import clear_mappers

from app.models.data_models import User
from app.services.unit_of_work import DEFAULT_SESSION_FACTORY


@pytest.fixture
def session():
    yield DEFAULT_SESSION_FACTORY()
    clear_mappers()
