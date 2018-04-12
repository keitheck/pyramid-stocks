from .association import association_table
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Index,
    ForeignKey,
    Text,
)

from .meta import Base


class My_stocks(Base):
    __tablename__ = 'stock_entries'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    description = Column(String)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)
    website = Column(String)
    account_id = relationship('Account', secondary=association_table, back_populates='stock_id')


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
