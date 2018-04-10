from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'account_entries'
    id = Column(Integer, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
    username = Column(String)



# Index('my_index', MyModel.name, unique=True, mysql_length=255)
