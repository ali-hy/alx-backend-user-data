#!/usr/bin/env python3
"""DB module
"""
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password are required")

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> User:
        """Find a user by a given attribute
        """
        query = self._session.query(User)

        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError

            query = query.filter(getattr(User, key) == kwargs[key])

        user = query.first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """Update a user
        """
        user = self.find_user_by(id=user_id)

        for key in kwargs:
            if not hasattr(user, key):
                raise ValueError

            setattr(user, key, kwargs[key])

        self._session.commit()
