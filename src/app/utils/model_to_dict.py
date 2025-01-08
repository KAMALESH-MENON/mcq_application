from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy.orm import class_mapper


def model_to_dict(model):
    """
    Converts an SQLAlchemy model instance to a dictionary with custom formatting.

    Args:
        model (SQLAlchemy model instance): The SQLAlchemy model instance to convert.

    Returns:
        dict: A dictionary representation of the model with formatted values.
    """
    raw_dict = {
        col.key: getattr(model, col.key)
        for col in class_mapper(model.__class__).mapped_table.columns
    }

    formatted_dict = {}
    for key, value in raw_dict.items():
        if isinstance(value, UUID):
            formatted_dict[key] = str(value)
        elif isinstance(value, Enum):
            formatted_dict[key] = value.value
        elif isinstance(value, datetime):
            formatted_dict[key] = (
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
                value.second,
                value.microsecond,
            )
        elif isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            try:
                formatted_dict[key] = eval(value)
            except Exception:
                formatted_dict[key] = value
        else:
            formatted_dict[key] = value

    return formatted_dict
