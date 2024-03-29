from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, create_engine, event, Float
from sqlalchemy.types import DateTime
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


SMALLINT = 40
BIGINT = 500

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True)
    title = Column(String(SMALLINT), nullable=False, unique=True)
    home_description = Column(String(BIGINT), nullable=False, unique=True)

@event.listens_for(SiteSettings.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        SiteSettings(title='Scout Market', home_description="Hi, welcome to the Scout Market ! It's here to help you to exchange your scouting equipment with other member of the unit. You can sell, buy, exchange, or even give your equipment."),
    ])
    session.commit()

class SiteColors(Base):
    __tablename__ = "site_colors"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    value = Column(String(SMALLINT), nullable=False)
    value_dark = Column(String(SMALLINT), nullable=True)

@event.listens_for(SiteColors.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        SiteColors(name='textPrimaryColor', value='#000000', value_dark='#ffffff'),
        SiteColors(name='textSecondaryColor', value='#ffffff', value_dark='#000000'),
        SiteColors(name='primaryColor', value='#ffffff', value_dark='#2d2d30'),
        SiteColors(name='secondaryColor', value='#8ABD91', value_dark='#8ABD91'),
        SiteColors(name='tertiaryColor', value='#009f83', value_dark='#009f83'),
        SiteColors(name='shadowColor', value='#2d2d30', value_dark='#ffffff'),
        SiteColors(name='validationColor', value='#00ff00', value_dark='#00ff00'),
        SiteColors(name='cancelColor', value='#ff0000', value_dark='#ff0000'),
        SiteColors(name='disabledColor', value='#636363', value_dark='#636363'),
    ])
    session.commit()

class SelectionsGroups(Base):
    __tablename__ = "selections_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class Selections(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))
    selections_groups_id = Column(Integer, ForeignKey("selections_groups.id"))

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
    display_name = Column(String(SMALLINT), nullable=False)
    description = Column(String(BIGINT))
    is_required = Column(Boolean, nullable=False)
    is_filterable = Column(Boolean, nullable=False)
    is_shown = Column(Boolean, nullable=False, default=True)
    type_id = Column(Integer, ForeignKey("types.id"))
    selections_groups_id = Column(Integer, ForeignKey("selections_groups.id"), nullable=True)

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
        States(name='archived'),
        States(name='deleted')
    ])
    session.commit()

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(SMALLINT), nullable=False, unique=True)
    description = Column(String(BIGINT))

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(SMALLINT), nullable=False, unique=True)
    email = Column(String(SMALLINT), unique=True)
    contact = Column(String(SMALLINT))
    password = Column(String(BIGINT), nullable=False)
    salt = Column(String(SMALLINT), nullable=False)
    states_id = Column(Integer, ForeignKey("states.id"))
    roles_id = Column(Integer, ForeignKey("roles.id"))

@event.listens_for(Users.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Users(username='admin', email='admin@outlook.com', password='d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892', salt='admin', states_id=1, roles_id=3),
    ])
    session.commit()

@event.listens_for(Roles.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Roles(name='Visitor'),
        Roles(name='User'),
        Roles(name='Administrator')
    ])
    session.commit()

class Offers(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    states_id = Column(Integer, ForeignKey("states.id"))

class FavoriteOffers(Base):
    __tablename__ = "favorite_offers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    offer_id = Column(Integer, ForeignKey("offers.id"))

class ValuesString(Base):
    __tablename__ = "values_string"

    id = Column(Integer, primary_key=True)
    value = Column(String(SMALLINT), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))

class ValuesInt(Base):
    __tablename__ = "values_int"

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))

class ValuesFloat(Base):
    __tablename__ = "values_float"

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))

class ValuesBool(Base):
    __tablename__ = "values_bool"

    id = Column(Integer, primary_key=True)
    value = Column(Boolean, nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
