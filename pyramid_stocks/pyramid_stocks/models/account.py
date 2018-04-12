from .meta import Base
from datetime import datetime as dt   
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt
from .association import association_table
from sqlalchemy.orm import relationship


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
)


manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    stock_id = relationship('My_stock', secondary=association_table, back_populates='account_id')

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = manager.encode(password, 10)
        self.registered_on = dt.now()
        self.admin = admin


    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        if request.dbsession is None:
            raise DBAPIError

        is_authenticated = False

        query = request.dbsession.query(cls).filter(cls.username == username).one_or_none()
        
        if query is not None:
            if manager.check(query.password, password):
                is_authenticated = True
                return (is_authenticated, username)

        return (is_authenticated, username)        


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
