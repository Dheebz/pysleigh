"""
Contains the base class for SQLAlchemy models.

The base class is used to define the structure of the database tables
and provides a common interface for all models in the application.
The base class is created using the declarative_base function from SQLAlchemy,
which allows for the creation of ORM models with a declarative syntax.


"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class is used to define the structure of the database tables
    and provides a common interface for all models in the application.

    """
