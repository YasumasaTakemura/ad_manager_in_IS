from sqlalchemy import create_engine, MetaData, Index
from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, TypeDecorator
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, mapper, relation, aliased, validates
from sqlalchemy.ext.declarative import declarative_base
import datetime
import pytz
import bcrypt
import logging
import os
import json
from dictalchemy import DictableModel
from dictalchemy.utils import make_class_dictable
from utils.funcs import today, begging_of_month

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('sqlalchemy.engine.base').setLevel(logging.DEBUG)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
try:
    print('>>>>>>>>>>>>>>SQLALCHEMY_DATABASE_URI')
    print(SQLALCHEMY_DATABASE_URI)
except:
    print('>>>>>>>> ERROR')
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{id}:{pw}@/{db}'.format(id='YasumasaTakemura', pw='yasu0708',
    #                                                                          db='test_20170408')

engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=QueuePool, echo=False)

metadata = MetaData()
metadata.bind = engine
Session = sessionmaker(autoflush=False, bind=engine)
DBSession = scoped_session(sessionmaker())
session = Session()
conn = engine.connect()

Base = declarative_base(cls=DictableModel)
Base = make_class_dictable(Base)

timezone = 'Asia/Tokyo'
now = datetime.datetime.now(pytz.timezone(timezone))


def find_account_name(id):
    try:
        name = session.query(AdAccount.account_name).filter(AdAccount.id == id).first()
        return name[0]
    except:
        return False


def find_account_id(name):
    try:
        _id = session.query(AdAccount.id).filter(AdAccount.account_name == name).first()
        return _id[0]
    except:
        return False


def find_media_name(id):
    try:
        name = session.query(AdMedia.media_name).filter(AdMedia.id == id).first()
        return name[0]
    except:
        return False


def find_media_id(name):
    try:
        _id = session.query(AdMedia.id).filter(AdMedia.media_name == name).first()
        return _id[0]
    except:
        return False


def find_product_name(id):
    try:
        name = session.query(Products.product_name).filter(Products.id == id).first()
        return name[0]
    except:
        return False


def find_product_id(name):
    try:
        _id = session.query(Products.id).filter(Products.product_name == name).first()
        return _id[0]
    except:
        return False


class PasswordHash(object):
    def __init__(self, hash_):
        assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
        assert hash_.count('$'), 'bcrypt hash should have 3x "$".'
        self.hash = str(hash_)
        self.rounds = int(self.hash.split('$')[2])

    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash."""
        if isinstance(candidate, str):
            if isinstance(candidate, str):
                candidate = candidate.encode('utf8')
                return bcrypt.hashpw(candidate, self.hash) == self.hash

        if isinstance(candidate, json):
            if isinstance(candidate, json):
                return bcrypt.hashpw(candidate, self.hash) == self.hash

        return False

    def __repr__(self):
        """Simple object representation."""
        return '<{}>'.format(type(self).__name__)

    @classmethod
    def new(cls, password, rounds):
        """Creates a PasswordHash from the given password."""
        if isinstance(password, str):
            password = password.encode('utf8')
        return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))

#
# class Password(TypeDecorator):
#     """Allows storing and retrieving password hashes using PasswordHash."""
#     impl = String
#
#     def __init__(self, rounds=12, **kwds):
#         self.rounds = rounds
#         super(Password, self).__init__(**kwds)
#
#     def process_bind_param(self, value, dialect):
#         """Ensure the value is a PasswordHash and then return its hash."""
#         return self._convert(value).hash
#
#     def process_result_value(self, value, dialect):
#         """Convert the hash to a PasswordHash, if it's non-NULL."""
#         if value is not None:
#             return PasswordHash(value)
#
#     def validator(self, password):
#         """Provides a validator/converter for @validates usage."""
#         return self._convert(password)
#
#     def _convert(self, value):
#         """Returns a PasswordHash from the given string.
#
#         PasswordHash instances or None values will return unchanged.
#         Strings will be hashed and the resulting PasswordHash returned.
#         Any other input will result in a TypeError.
#         """
#         if isinstance(value, PasswordHash):
#             return value
#         elif isinstance(value, str):
#             return PasswordHash.new(value, self.rounds)
#         elif value is not None:
#             raise TypeError(
#                 'Cannot convert {} to a PasswordHash'.format(type(value)))
#
#
# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     password = Column(Password)
#
#     # Or specify a cost factor other than the default 12
#     # password = Column(Password(rounds=10))
#
#     @validates('password')
#     def _validate_password(self, key, password):
#         return getattr(type(self), key).type.validator(password)
#

########################
#  Password and Tokens
########################
class PasswordAndToken(Base):
    __tablename__ = 'password_and_token'
    id = Column(Integer, autoincrement=True, primary_key=True)
    media_name = Column(String, nullable=False, )
    type = Column(String, nullable=False, )
    value = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)
    #
    # @validates('password')
    # def _validate_password(self, key, value):
    #     return getattr(type(self), key).type.validator(value)


########################
# Conjunction
########################

class Promotion(Base):
    __tablename__ = 'promotion'
    __table_args__ = (UniqueConstraint('account_id', 'product_id', 'media_id', 'device_id', name='u_promotion'),)
    id = Column(Integer, autoincrement=True, primary_key=True)
    account_id = Column(Integer, ForeignKey('ad_account.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    media_id = Column(Integer, ForeignKey('ad_media.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)

    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    # AdMedia = relationship('AdMedia')
    # Device = relationship('Device')
    # Staff = relationship('Staff')
    # Istool = relationship('Istool')
    # AdAccount = relationship('AdAccount')
    # Products = relationship('Products')
    # AdFee = relationship('AdFee',cascade='all, delete-orphan')
    # DailyBudget = relationship('DailyBudget',cascade='all, delete-orphan')
    # MonthlyBudget = relationship('MonthlyBudget',cascade='all, delete-orphan')
    # CampaignReport = relationship('CampaignReport',cascade='all, delete-orphan')
    # AdReportManager = relationship('AdReportManager')


########################
# Low Layer
########################
class AdAccount(Base):
    __tablename__ = 'ad_account'
    id = Column(Integer, autoincrement=True, primary_key=True)
    account_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    Products = relationship('Products')
    Promotion = relationship('Promotion')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (UniqueConstraint('account_id', 'product_name', name='unique_product'),)
    id = Column(Integer, autoincrement=True, primary_key=True)
    account_id = Column(Integer, ForeignKey('ad_account.id'), nullable=False)
    product_name = Column(String, nullable=False, unique=False)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    Promotion = relationship('Promotion')
    AdAccount = relationship('AdAccount')


class AdMedia(Base):
    __tablename__ = 'ad_media'
    id = Column(Integer, autoincrement=True, primary_key=True)
    media_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    Promotion = relationship('Promotion')
    # MediaCampaignIDs = relationship('MediaCampaignIDs')


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, autoincrement=True, primary_key=True)
    device = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    Promotion = relationship('Promotion')


########################
# Mid Layer
########################

# at first time, only promotion is is needed
class AdFee(Base):
    __tablename__ = 'ad_fee'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    cases = Column(String, nullable=False, default='times')
    fee = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)


# at first time, only promotion is is needed
class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    staff = Column(String, nullable=False, default='------', unique=True)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)


# at first time, only promotion is is needed
class DailyBudget(Base):
    __tablename__ = 'daily_budget'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=today())
    budget = Column(Integer, nullable=False, default=0)
    scope = Column(String, nullable=False, default='media')
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    # Promotion = relationship('Promotion')


# at first time, only promotion is is needed
class MonthlyBudget(Base):
    __tablename__ = 'monthly_budget'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    month = Column(DateTime, nullable=False, default=begging_of_month())
    budget = Column(Integer, nullable=False, default=0)
    scope = Column(String, nullable=False, default='media')
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    # Promotion = relationship('Promotion')


# at first time, only promotion is is needed
class AnnualBudget(Base):
    __tablename__ = 'annual_budget'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    annual = Column(DateTime, nullable=False, default=begging_of_month())
    budget = Column(Integer, nullable=False, default=0)
    scope = Column(String, nullable=False, default='media')
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    # Promotion = relationship('Promotion')


class AdReportManager(Base):
    __tablename__ = 'ad_report_manager'

    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, nullable=False)
    media_account_id = Column(String, nullable=False)
    media_campaign_id = Column(String, nullable=True)
    reporting = Column(Boolean, nullable=True, default=True)
    type = Column(String, nullable=False, default='account')  # campaign or creative
    schedule = Column(String, nullable=False, default='day')
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    # Promotion = relationship('Promotion')
    __table_args__ = (
        UniqueConstraint('promotion_id', 'media_account_id', 'media_campaign_id', name='unique_ad_report_manager'),)

    # MediaCampaignIDs = relationship('MediaCampaignIDs')


# class MediaAccountIDs(Base):
#     __tablename__ = 'media_account_ids'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     ad_account_id = Column(Integer, ForeignKey('ad_account.id'), nullable=False)
#     media_account_id = Column(String, nullable=False)
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     AdAccount = relationship('AdAccount')
#
#
# class MediaCampaignIDs(Base):
#     __tablename__ = 'media_campaign_ids'
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     media_account_id = Column(Integer, ForeignKey('media_account_ids.id'), nullable=False)
#     campaign_name = Column(String, nullable=False)
#     media_campaign_id = Column(String, nullable=False)
#     # media_id = Column(String, ForeignKey('ad_media.id'), nullable=False)
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     MediaAccountID = relationship('MediaAccountID')
# AdMedia = relationship('AdMedia')


class AdjustEvents(Base):
    __tablename__ = 'adjust_events'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=True)
    key = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    __table_args__ = (UniqueConstraint('date', 'promotion_id', name='unique_adjust'),)


# at first time, only promotion is is needed
class Istool(Base):
    __tablename__ = 'istool'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=False)
    program_name = Column(String, nullable=False, default='------')
    program_id = Column(String, nullable=False, default='000000')
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    __table_args__ = (UniqueConstraint('program_name', 'program_id', name='unique_istool'),)


########################
# Report
########################
class CampaignReport(Base):
    __tablename__ = 'campaign_report'
    id = Column(Integer, autoincrement=True, primary_key=True)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=True)
    date = Column(String, nullable=False)
    campaign_name = Column(String, nullable=False)
    campaign_id = Column(String, nullable=True)
    adset_name = Column(String, nullable=True, default='untitled')
    adset_id = Column(String, nullable=True)
    spend = Column(Integer, nullable=True, default=0)
    impressions = Column(Integer, nullable=True, default=0)
    clicks = Column(Integer, nullable=True, default=0)
    cvs = Column(Integer, nullable=True, default=0)
    installs = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, default=now)
    updated_at = Column(DateTime, default=now, onupdate=now)

    Promotion = relationship('Promotion')
    __table_args__ = (
        UniqueConstraint('date', 'promotion_id', 'campaign_id', 'adset_id', name='unique_campaign_report'),)


Base.metadata.create_all(bind=engine)
engine.dispose()
