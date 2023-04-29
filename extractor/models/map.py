"""Core models."""

import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON, TEXT, INTEGER, BOOLEAN, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
Base = declarative_base()


class User(Base):
    """User class."""

    __tablename__ = 'user'
    id = Column(TEXT, primary_key=True, nullable=False)
    name = Column(TEXT, nullable=False)

class Source(Base):
    """Sources class"""

    __tablename__ = 'sources'
    id = Column(TEXT, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(TEXT, nullable=False)
    index_name = Column(TEXT, nullable=False)
    target_field = Column(TEXT, nullable=False)
    search_object = Column(JSON, nullable=True)

class SourceField(Base):
    """Sources fields."""

    __tablename__ = 'source_fields'
    id = Column(TEXT, primary_key=True, nullable=False, default=uuid.uuid4)
    source_id = Column(TEXT, ForeignKey('sources.id'), nullable=True)
    name = Column(TEXT, nullable=False)
    operations = Column(JSON, nullable=True)



class Objects(Base):
    """Objects class."""

    __tablename__ = 'obj'
    id = Column(TEXT, primary_key=True, nullable=False)
    obj_parent_id = Column(TEXT, ForeignKey('obj.id'), nullable=True)
    created_utc = Column(TIMESTAMP, nullable=False)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable = False)
