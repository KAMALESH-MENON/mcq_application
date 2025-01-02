from sqlalchemy.orm import class_mapper


def model_to_dict(model):
    """
    Converts an SQLAlchemy model instance to a dictionary.

    Args:
        model (SQLAlchemy model instance): The SQLAlchemy model instance to convert.

    Returns:
        dict: A dictionary representation of the model.
    """
    return {
        col.key: getattr(model, col.key)
        for col in class_mapper(model.__class__).mapped_table.columns
    }
