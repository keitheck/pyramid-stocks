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


association_table = Table('association_table', Base.metadata,
    Column('stock_id', Integer, ForeignKey('stock_entries.id')),
    Column('account_id', Integer, ForeignKey('accounts.id'))
)
