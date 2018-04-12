from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    Table,
)

from .meta import Base


association_table = Table('association', Base.metadata,
    Column('stock_id', Integer, ForeignKey('stock.id')),
    Column('account_id', Integer, ForeignKey('account.id'))
)
