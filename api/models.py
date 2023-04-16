from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, create_engine, event
from sqlalchemy.types import Date
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


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

@event.listens_for(Types.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Types(name='int'),
        Types(name='string'),
        Types(name='float'),
        Types(name='bool'),
        Types(name='date'),
        Types(name='time'),
        Types(name='datetime'),
        Types(name='selection'),
        Types(name='multiselection'),
        Types(name='file'),
        Types(name='image'),
        Types(name='video'),
        Types(name='audio'),
        Types(name='url'),
        Types(name='email'),
        Types(name='phone'),
        Types(name='address'),
        Types(name='location'),
        Types(name='color')
    ])
    session.commit()

class Fields(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False)
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

class States(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

@event.listens_for(States.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        States(name='to_validate'),
        States(name='active'),
        States(name='archived')
    ])
    session.commit() 

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(SMALLINT), nullable=False, unique=True)
    email = Column(String(SMALLINT), nullable=False, unique=True)
    password = Column(String(BIGINT), nullable=False)
    salt = Column(String(SMALLINT), nullable=False)
    states_id = Column(Integer, ForeignKey("states.id"))

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class UserRoles(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

class Offers(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    states_id = Column(Integer, ForeignKey("states.id"))

class Values(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True)
    value = Column(String(SMALLINT), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))


Base.metadata.create_all(bind=engine)
