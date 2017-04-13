import os
from flask import jsonify
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from sqlalchemy import asc, desc
from db.ads.ads import AdAccount, AdMedia, AdFee, Products, Promotion, DailyBudget, MonthlyBudget, \
    session, Staff, Istool, AdReportManager
from db.ads import ads
import json
from datetime import datetime, timedelta, time
import pytz
import re
from utils.funcs import (remove_specified_key,
                         replace_key_name,
                         add_fields,
                         pickup_specified_key,
                         cast_to_dict,
                         str_to_int)


class Updater:
    ##########################################
    # Update
    ##########################################
    @classmethod
    def update_ad_account(cls, id, name):

        try:
            target = session.query(AdAccount).filter(AdAccount.id == id).first()
            target.account_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
    @classmethod
    def update_ad_media(cls, id, name):

        try:
            target = session.query(AdMedia).filter(AdMedia.id == id).first()
            target.media_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    @classmethod
    def update_products(cls, id, name):

        try:
            target = session.query(Products).filter(Products.id == id).first()
            target.product_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    @classmethod
    def update_ad_fee(cls, id, **kwargs):
        session = ads.session

        try:
            target = session.query(AdFee).filter(AdFee.id == id).first()
            _fee = kwargs.get('fee', False)

            # _target = kwargs.get('target', False)
            # if target is not False:
            #     target.target = _target

            target.fee = _fee

            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()


    @classmethod
    def update_ad_budget(cls,**kwargs):
        session = ads.session

        _budget = kwargs.get('budget',False)

        try:
            target = session.query(MonthlyBudget).filter(MonthlyBudget.id == kwargs['id']).first()

            if _budget:
                target.budget = _budget

            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()

    @classmethod
    def update_staff(cls,**kwargs):
        session = ads.session

        _staff = kwargs.get('staff',False)

        try:
            target = session.query(Staff).filter(Staff.id == kwargs['id']).first()

            if _staff is not False:
                target.staff = _staff

            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()



    @classmethod
    def update_program_name(cls,**kwargs):
        session = ads.session

        _program_name = kwargs.get('program_name',False)

        try:
            target = session.query(Istool).filter(Istool.id == kwargs['id']).first()

            if _program_name is not False:
                target.program_name = _program_name

            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()



    @classmethod
    def update_program_id(cls,**kwargs):
        session = ads.session

        _program_id = kwargs.get('program_id',False)

        try:
            target = session.query(Istool).filter(Istool.id == kwargs['id']).first()

            if _program_id is not False:
                target.program_id = _program_id

            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()



    def update_ad_report_manager(self, id, reporting, media_campaign_id=None):

        res = session.query(AdReportManager.media_campaign_id).filter(AdReportManager.id == id).first()

        try:
            res.reporting = reporting

            if not res and media_campaign_id:
                res.media_campaign_id = media_campaign_id

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
