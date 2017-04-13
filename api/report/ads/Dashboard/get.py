import os
from sqlalchemy import delete,func, asc, desc,case,cast,Integer
from sqlalchemy.sql import label
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from db.ads.ads import AdAccount, AdMedia, AdFee, Products, Promotion, DailyBudget, MonthlyBudget, \
    Staff, Device, Istool,CampaignReport
from db.ads import ads
from utils.funcs import (parseSAtoJson,
                         json_to_csv,
                         end_of_month,
                         begging_of_month,
                         today,
                         remove_specified_key,
                         )
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


class Manager:
    @classmethod
    def get_promotion_list(cls):
        start_time = begging_of_month()
        end_time = end_of_month()
        start_time = start_time.strftime('%Y-%m-%d')
        end_time = end_time.strftime('%Y-%m-%d')

        promos = []
        session = ads.session
        ad_spend = func.sum(case([(AdFee.fee > 1, CampaignReport.spend * AdFee.fee), ],
                                 else_=CampaignReport.spend / AdFee.fee))

        all_promotion = session.query(
            AdAccount,
            Promotion,
            Products,
            AdMedia,
            Device,
            AdFee,
            MonthlyBudget,
            Staff,
            Istool,
            label('spend', cast(ad_spend,Integer)),
        ).filter(
            Promotion.account_id == AdAccount.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.device_id == Device.id,
            Promotion.id == AdFee.promotion_id,
            Promotion.id == MonthlyBudget.promotion_id,
            Promotion.id == Staff.promotion_id,
            Promotion.id == Istool.promotion_id,
            Promotion.id == CampaignReport.promotion_id,
            CampaignReport.date.between(start_time, end_time),
        ).group_by(
            AdAccount.id,
            Promotion.id,
            Products.id,
            AdMedia.id,
            Device.id,
            AdFee.id,
            MonthlyBudget.id,
            Staff.id,
            Istool.id,
        ).\
            order_by(asc(Promotion.id)).all()


        for i, promotion in enumerate(all_promotion):

            _promotion = {
                'promotion_id':  promotion.Promotion.id,
                'account_name': promotion.AdAccount.account_name,
                'account_id': promotion.AdAccount.id,
                'm_budget_id': promotion.MonthlyBudget.id,
                'm_budget': promotion.MonthlyBudget.budget,
                'month': promotion.MonthlyBudget.month,
                'device': promotion.Device.device,
                'device_id': promotion.Device.id,
                'fee': promotion.AdFee.fee,
                'fee_id': promotion.AdFee.id,
                'media_name': promotion.AdMedia.media_name,
                'media_id': promotion.AdMedia.id,
                'product_name': promotion.Products.product_name,
                'product_id': promotion.Products.id,
                'istool_id': promotion.Istool.id,
                'program_id': promotion.Istool.program_id,
                'program_name': promotion.Istool.program_name,
                'staff_id': promotion.Staff.id,
                'staff': promotion.Staff.staff,
                'spend': promotion.spend,
            }

            promos.append(_promotion)

        return promos

    @classmethod
    def get_promotion(cls,id):
        promos = []
        session = ads.session
        all_promotion = session.query(
            AdAccount,
            Promotion,
            Products,
            AdMedia,
            Device,
            AdFee,
            MonthlyBudget,
            Staff,
            Istool,
        ).filter(
            Promotion.id == id,
            Promotion.account_id == AdAccount.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.device_id == Device.id,
            Promotion.id == AdFee.promotion_id,
            Promotion.id == MonthlyBudget.promotion_id,
            Promotion.id == Staff.promotion_id,
            Promotion.id == Istool.promotion_id,

        ). \
            order_by(asc(Promotion.id)).all()
        for promotion in all_promotion:
            _promotion = {
                'promotion_id': promotion.Promotion.id,
                'account_name': promotion.AdAccount.account_name,
                'account_id': promotion.AdAccount.id,
                'm_budget_id': promotion.MonthlyBudget.id,
                'm_budget': promotion.MonthlyBudget.budget,
                'month': promotion.MonthlyBudget.month,
                'device': promotion.Device.device,
                'device_id': promotion.Device.id,
                'fee': promotion.AdFee.fee,
                'fee_id': promotion.AdFee.id,
                'media_name': promotion.AdMedia.media_name,
                'media_id': promotion.AdMedia.id,
                'product_name': promotion.Products.product_name,
                'product_id': promotion.Products.id,
                'istool_id': promotion.Istool.id,
                'program_id': promotion.Istool.program_id,
                'program_name': promotion.Istool.program_name,
                'staff_id': promotion.Staff.id,
                'staff': promotion.Staff.staff,
            }
            promos.append(_promotion)
        return promos
