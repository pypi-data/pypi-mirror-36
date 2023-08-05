"""A base class for SQLAlchemy-based repositories."""

from typing import Any, TypeVar

from kerno.kerno import Kerno

Entity = TypeVar('Entity')  # For generic functions. Can be any type.


class BaseSQLAlchemyRepository:
    """Base class for a SQLAlchemy-based repository."""

    def __init__(self, kerno: Kerno, session_factory: Any) -> None:
        """Construct a SQLAlchemy repository instance to serve ONE request.

        - ``kerno`` is the Kerno instance for the current application.
        - ``session_factory`` is a function that returns a
          SQLAlchemy session to be used in this request -- scoped or not.
        """
        self.kerno = kerno
        self.sas = self.new_sas(session_factory)

    def new_sas(self, session_factory):
        """Obtain a new SQLAlchemy session instance."""
        is_scoped_session = hasattr(session_factory, 'query')
        # Because we don't want to depend on SQLAlchemy:
        if callable(session_factory) and not is_scoped_session:
            return session_factory()
        else:
            return session_factory

    def add(self, entity: Entity) -> Entity:
        """Add an object to the SQLAlchemy session, then return it."""
        self.sas.add(entity)
        return entity

    def flush(self) -> None:
        """Obtain IDs on new objects and update state on the database.

        Without committing the transaction.
        """
        self.sas.flush()
