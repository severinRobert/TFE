from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, DateTime, Float
from sqlalchemy.types import Date
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SMALLINT = 40
BIGINT = 500

class SelectionsGroup(Base):
    __tablename__ = "selections_group"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class Selections(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))
    selections_group_id = Column(Integer, ForeignKey("selections_group.id"))

class Types(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class Fields(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))
    is_required = Column(Boolean, nullable=False)
    is_filterable = Column(Boolean, nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"))
    selections_group_id = Column(Integer, ForeignKey("selections_group.id"), nullable=True)

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class ProductFields(Base):
    __tablename__ = "product_fields"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))
    email = Column(String(SMALLINT), nullable=False, unique=True)
    password = Column(String(SMALLINT), nullable=False, unique=True)
    status_id = Column(Integer, ForeignKey("status.id"))

class Offers(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    status_id = Column(Integer, ForeignKey("status.id"))

class Values(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True)
    value = Column(String(SMALLINT), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))

