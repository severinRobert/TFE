from models import *
from datetime import datetime

############ SELECTIONS GROUPS ############
@event.listens_for(SelectionsGroup.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        SelectionsGroup(name='Colors', description='Colors'),
        SelectionsGroup(name='Brands', description='Brands'),
        SelectionsGroup(name='Size (clothing)', description='Clothes size'),
    ])
    session.commit()

############ SELECTIONS ############
@event.listens_for(Selections.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Selections(name='red', description='Red', selections_group_id=1),
        Selections(name='blue', description='Blue', selections_group_id=1),
        Selections(name='green', description='Green', selections_group_id=1),
        Selections(name='yellow', description='Yellow', selections_group_id=1),
        Selections(name='orange', description='Orange', selections_group_id=1),
        Selections(name='purple', description='Purple', selections_group_id=1),
        Selections(name='black', description='Black', selections_group_id=1),
        Selections(name='white', description='White', selections_group_id=1),
        Selections(name='brown', description='Brown', selections_group_id=1),
        Selections(name='gray', description='Gray', selections_group_id=1),
        Selections(name='pink', description='Pink', selections_group_id=1),
        Selections(name='Quechua', description='Quechua', selections_group_id=2),
        Selections(name='Van Rysel', description='Van Rysel', selections_group_id=2),
        Selections(name='Forclaz', description='Forclaz', selections_group_id=2),
        Selections(name='Tribord', description='Tribord', selections_group_id=2),
        Selections(name='XS', selections_group_id=3),
        Selections(name='S', selections_group_id=3),
        Selections(name='M', selections_group_id=3),
        Selections(name='L', selections_group_id=3),
        Selections(name='XL', selections_group_id=3),
    ])
    session.commit()

############ FIELDS ############
@event.listens_for(Fields.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Fields(name='Price', description='Price', is_required=True, is_filterable=True, type_id=3, selections_group_id=None),
        Fields(name='Color', description='Color', is_required=False, is_filterable=True, type_id=8, selections_group_id=1),
        Fields(name='Weight (kg)', description='Weight', is_required=False, is_filterable=True, type_id=3, selections_group_id=None),
        Fields(name='Brand', description='Brand', is_required=False, is_filterable=True, type_id=8, selections_group_id=2),
        Fields(name='Is waterproof', description='', is_required=False, is_filterable=True, type_id=4, selections_group_id=None),
        Fields(name='Volume (L)', description='The capacity in litre', is_required=False, is_filterable=True, type_id=3, selections_group_id=None),
        Fields(name='Number of places', description='', is_required=False, is_filterable=True, type_id=1, selections_group_id=None),
        Fields(name='Size (clothing)', description='Clothe size', is_required=True, is_filterable=True, type_id=8, selections_group_id=3),
        Fields(name='Size (foot)', description='Foot size', is_required=True, is_filterable=True, type_id=1, selections_group_id=None),
        Fields(name='Length (cm)', description='Length', is_required=False, is_filterable=True, type_id=1, selections_group_id=None),
    ])
    session.commit()

############ PRODUCTS ############
@event.listens_for(Products.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Products(name='Tent'),
        Products(name='Baladin pullover'),
        Products(name='Jacket'),
        Products(name='Hicking boots'),
        Products(name='Socks'),
        Products(name='Sleeping bag'),
        Products(name='Bottle'),
    ])
    session.commit()

############ PRODUCT_FIELDS ############
@event.listens_for(ProductFields.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        # Tent
        ProductFields(product_id=1, field_id=1),
        ProductFields(product_id=1, field_id=2),
        ProductFields(product_id=1, field_id=3),
        ProductFields(product_id=1, field_id=4),
        ProductFields(product_id=1, field_id=7),
        # Baladin pullover
        ProductFields(product_id=2, field_id=1),
        ProductFields(product_id=2, field_id=2),
        ProductFields(product_id=2, field_id=4),
        ProductFields(product_id=2, field_id=8),
        # Jacket
        ProductFields(product_id=3, field_id=1),
        ProductFields(product_id=3, field_id=2),
        ProductFields(product_id=3, field_id=4),
        ProductFields(product_id=3, field_id=8),
        # Hicking boots
        ProductFields(product_id=4, field_id=1),
        ProductFields(product_id=4, field_id=2),
        ProductFields(product_id=4, field_id=4),
        ProductFields(product_id=4, field_id=9),
        # Socks
        ProductFields(product_id=5, field_id=1),
        ProductFields(product_id=5, field_id=2),
        ProductFields(product_id=5, field_id=4),
        ProductFields(product_id=5, field_id=9),
        # Sleeping bag
        ProductFields(product_id=6, field_id=1),
        ProductFields(product_id=6, field_id=2),
        ProductFields(product_id=6, field_id=4),
        ProductFields(product_id=6, field_id=10),
    ])
    session.commit()

############ USERS ############
@event.listens_for(Users.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Users(username='admin', email='admin@outlook.com', password='d82494f05d6917ba02f7aaa29689ccb444bb73f20380876cb05d1f37537b7892', salt='admin', states_id=1),
        Users(username='user', email='user@outlook.com', password='e172c5654dbc12d78ce1850a4f7956ba6e5a3d2ac40f0925fc6d691ebb54f6bf', salt='user', states_id=1),
        Users(username='scout', email='scout@outlook.com', password='0813fa9c43fbf4c2c012b6274a1f3b7971825c6c52623468f7422dd66ccc9e3d', salt='scout', states_id=1),
    ])
    session.commit()

############ USER_ROLES ############
@event.listens_for(UserRoles.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        UserRoles(user_id=1, role_id=3),
        UserRoles(user_id=2, role_id=2),
        UserRoles(user_id=3, role_id=2),
    ])
    session.commit()

############ OFFERS ############
@event.listens_for(Offers.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        Offers(owner_id=2, product_id=1, states_id=3, start_datetime=datetime(2020, 1, 1, 0, 0, 0), end_datetime=datetime(2020, 1, 2, 0, 0, 0)),
        Offers(owner_id=2, product_id=2, states_id=3, start_datetime=datetime(2021, 10, 30, 0, 0, 0), end_datetime=datetime(2021, 12, 2, 0, 0, 0)),
        Offers(owner_id=2, product_id=3, states_id=2, start_datetime=datetime(2023, 3, 1, 0, 0, 0)),
        Offers(owner_id=3, product_id=4, states_id=2, start_datetime=datetime(2022, 8, 27, 0, 0, 0), end_datetime=datetime(2022, 11, 5, 0, 0, 0)),
        Offers(owner_id=3, product_id=5, states_id=2, start_datetime=datetime(2023, 3, 1, 0, 0, 0)),
        Offers(owner_id=3, product_id=4, states_id=2, start_datetime=datetime(2023, 3, 1, 0, 0, 0)),
    ])
    session.commit()

############ VALUES ############
@event.listens_for(ValuesInt.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        ValuesInt(offer_id=1, field_id=2, value=1),
        ValuesInt(offer_id=1, field_id=4, value=1),
        ValuesInt(offer_id=1, field_id=7, value=2),
        ValuesInt(offer_id=2, field_id=2, value=2),
        ValuesInt(offer_id=2, field_id=4, value=2),
        ValuesInt(offer_id=2, field_id=8, value=2),
        ValuesInt(offer_id=3, field_id=2, value=1),
        ValuesInt(offer_id=3, field_id=4, value=3),
        ValuesInt(offer_id=3, field_id=8, value=3),
        ValuesInt(offer_id=4, field_id=2, value=2),
        ValuesInt(offer_id=4, field_id=4, value=1),
        ValuesInt(offer_id=4, field_id=9, value=36),
        ValuesInt(offer_id=5, field_id=2, value=3),
        ValuesInt(offer_id=5, field_id=4, value=1),
        ValuesInt(offer_id=5, field_id=9, value=38),
        ValuesInt(offer_id=6, field_id=2, value=2),
        ValuesInt(offer_id=6, field_id=4, value=1),
        ValuesInt(offer_id=6, field_id=9, value=34),
    ])
    session.commit()

@event.listens_for(ValuesFloat.__table__, 'after_create')
def insert_initial_values(target, connection, **kw):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()
    session.add_all([
        ValuesFloat(offer_id=1, field_id=1, value=35),
        ValuesFloat(offer_id=1, field_id=3, value=2.5),
        ValuesFloat(offer_id=2, field_id=1, value=15),
        ValuesFloat(offer_id=3, field_id=1, value=25),
        ValuesFloat(offer_id=4, field_id=1, value=25),
        ValuesFloat(offer_id=5, field_id=1, value=1),
        ValuesFloat(offer_id=6, field_id=1, value=20),
    ])
    session.commit()

