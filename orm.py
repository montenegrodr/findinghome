from sqlalchemy import create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, DateTime, Float
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Dwelling(Base):
    __tablename__ = 'dwelling'

    id                 = Column(Integer, primary_key=True)
    address_line_1     = Column(String)
    address_line_2     = Column(String)
    area_size          = Column(String)
    contact_number     = Column(String)
    county             = Column(String)
    daft_link          = Column(String)
    dwelling_type      = Column(String)
    facilities         = Column(TEXT)
    formalised_address = Column(TEXT)
    listing_image      = Column(String)
    num_bathrooms      = Column(Integer)
    num_bedrooms       = Column(Integer)
    price              = Column(String)
    price_change       = Column(String)
    price_number       = Column(Integer)
    price_month        = Column(Integer)
    timestamp          = Column(DateTime)
    town               = Column(String)
    viewings           = Column(String)
    features           = Column(String)
    agent              = Column(String)
    agent_url          = Column(String)
    posted_since       = Column(String)
    lat                = Column(Float)
    long               = Column(Float)
    hash               = Column(String)


class Dataset(object):
    def __init__(self, **kwargs):
        self.conection_string = kwargs['con_str']
        self.eng      = self._create_eng()
        self.session = None

        Base.metadata.bind = self.eng
        Base.metadata.create_all()

    def open_session(self):
        self.session = self._create_session()

    def close_session(self):
        if self.session:
            self.session.close()

    def commit(self):
        self.session.commit()

    def insert(self, obj):
        self.session.add(obj)

    def _create_eng(self):
        return create_engine(self.conection_string)

    def _create_session(self):
        return sessionmaker(bind=self.eng)()

    def exists(self, h):
        return self.session.query(
            exists().where(Dwelling.hash == h)
        ).scalar()


class DataController(object):
    def __init__(self, con_str):
        self.ds = Dataset(con_str=con_str)

    def __enter__(self):
        self.ds.open_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ds.close_session()

    def insert(self, doc):
        if self.ds.exists(doc.get('hash')):
            return
        self.ds.insert(Dwelling(
            address_line_1=doc.get('address_line_1'),
            address_line_2=doc.get('address_line_2'),
            area_size=doc.get('area_size'),
            contact_number=doc.get('contact_number'),
            county=doc.get('county'),
            daft_link=doc.get('daft_link'),
            dwelling_type=doc.get('dwelling_type'),
            facilities=','.join(doc.get('facilities', [])),
            formalised_address=doc.get('formalised_address'),
            listing_image=doc.get('listing_image'),
            num_bathrooms=doc.get('num_bathrooms'),
            num_bedrooms=doc.get('num_bedrooms'),
            price=doc.get('price'),
            price_change=doc.get('price_change'),
            price_number=doc.get('price_number'),
            price_month=doc.get('price_month'),
            timestamp=doc.get('timestamp'),
            town=doc.get('town'),
            viewings=','.join(doc.get('viewings', [])),
            features=doc.get('features'),
            agent=doc.get('agent'),
            agent_url=doc.get('agent_url'),
            posted_since=doc.get('posted_since'),
            hash=doc.get('hash'),
        ))
        self.ds.commit()