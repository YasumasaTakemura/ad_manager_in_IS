from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, Sequence, types, Float
from sqlalchemy import func, asc, case, and_, subquery
from sqlalchemy.sql import label
from sqlalchemy.orm import aliased
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.sql.expression import cast
from report.scraper.scraper.Scraper import Scraper
from decimal import Decimal
from db.ads.ads import Products, AdMedia, AdAccount, AdReportManager, AdjustEvents, CampaignReport, \
    DailyBudget, MonthlyBudget, AdFee, Promotion, Device
from db.ads import ads
from db.ads.ads import find_account_name, find_account_id, find_media_id, find_media_name, find_product_id, \
    find_product_name
from utils.funcs import (parseSAtoJson,
                         json_to_csv,
                         end_of_month,
                         begging_of_month,
                         today,
                         remove_specified_key,
                         )
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from report.ads.Manager.manager import AdAPItManager
import json


class Dashboard:
    start_time = begging_of_month()
    end_time = today()
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')

    @classmethod
    def init_resister(cls, start_time=start_time, end_time=end_time):
        session = ads.session

        ad_spend = cast(func.sum(case([(AdFee.fee > 1, CampaignReport.spend * AdFee.fee), ],
                                 else_=CampaignReport.spend / AdFee.fee)),Integer)

        kpis = session.query(
            AdFee.fee,
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name,
            Device.device,
            Products.product_name,
            label('spend', ad_spend),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
            label('cpi', ad_spend / Decimal(func.sum(CampaignReport.cvs))),
            label('ctr', cast(func.sum(CampaignReport.clicks),Float) / cast(func.sum(CampaignReport.impressions,Float))),
            label('cvr', cast(func.sum(CampaignReport.cvs),Float)  / cast(func.sum(CampaignReport.clicks),Float) ),
        ).group_by(
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name,
            Device.device,
            Products.product_name,
        ).filter(
            CampaignReport.promotion_id == Promotion.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.device_id == Device.id,
            Promotion.id == AdFee.promotion_id,
        ).having(CampaignReport.date.between(start_time, end_time)).order_by(asc(CampaignReport.promotion_id)).all()

        header = [
            'fee',
            'promotion_id',
            'date',
            'media_name',
            'device',
            'product_name',
            'spend',
            'impressions',
            'clicks',
            'cvs',
            'cpi',
            'ctr',
            'cvr',

        ]

        return header, kpis

    @classmethod
    def get_daily_report_by_promotion(cls, start_time=start_time, end_time=end_time):
        session = ads.session

        ad_spend = cast(func.sum(case([(AdFee.fee > 1, CampaignReport.spend * AdFee.fee), ],
                                 else_=CampaignReport.spend / AdFee.fee)),Integer)

        kpis = session.query(
            AdFee.fee,
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name,
            Device.device,
            Products.product_name,
            label('spend', ad_spend),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
            label('ctr',
                  cast(func.sum(CampaignReport.clicks), Float) / cast(func.sum(CampaignReport.impressions), Float)),
            label('cvr', cast(func.sum(CampaignReport.cvs), Float) / cast(func.sum(CampaignReport.clicks), Float)),

        ).group_by(
            AdFee.fee,
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name,
            Device.device,
            Products.product_name,
        ).filter(
            CampaignReport.promotion_id == Promotion.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.device_id == Device.id,
            Promotion.id == AdFee.promotion_id,
        ).having(CampaignReport.date.between(start_time, end_time)).order_by(asc(CampaignReport.promotion_id)).all()

        header = [
            'fee',
            'promotion_id',
            'date',
            'media_name',
            'device',
            'product_name',
            'spend',
            'impressions',
            'clicks',
            'cvs',
            'cpi',
            'ctr',
            'cvr',
        ]

        return header, kpis

    @classmethod
    def get_report_by_media(cls, start_time=start_time, end_time=end_time):
        session = ads.session

        ad_spend = cast(func.sum(case([(AdFee.fee > 1, CampaignReport.spend * AdFee.fee), ],
                                 else_=CampaignReport.spend / AdFee.fee)),Integer)

        kpis = session.query(
            AdFee.fee,
            AdMedia.media_name,
            Products.product_name,
            Device.device,
            label('spend', ad_spend),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
            label('ctr',
                  cast(func.sum(CampaignReport.clicks), Float) / cast(func.sum(CampaignReport.impressions), Float)),
            label('cvr', cast(func.sum(CampaignReport.cvs), Float) / cast(func.sum(CampaignReport.clicks), Float)),

        ).group_by(
            AdFee.fee,
            CampaignReport.promotion_id,
            AdMedia.media_name,
            Device.device,
            Products.product_name,
        ).filter(
            CampaignReport.promotion_id == Promotion.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.device_id == Device.id,
            Promotion.id == AdFee.promotion_id,
            CampaignReport.date.between(start_time, end_time),
        ).order_by(asc(Products.product_name)).all()

        header = [
            'fee',
            'media_name',
            'product_name',
            'device',
            'spend',
            'impressions',
            'clicks',
            'cvs',
            'cpi',
            'ctr',
            'cvr',
        ]

        return header, kpis

    @classmethod
    def get_report_by_product(cls, start_time=start_time, end_time=end_time):
        session = ads.session

        ad_spend = cast(func.sum(case([(AdFee.fee > 1, CampaignReport.spend * AdFee.fee), ],
                                 else_=CampaignReport.spend / AdFee.fee)),Integer)

        kpis = session.query(
            AdFee.fee,
            Products.product_name,
            label('spend', ad_spend),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
            label('ctr',cast(func.sum(CampaignReport.clicks), Float) / cast(func.sum(CampaignReport.impressions), Float)),
            label('cvr',cast(func.sum(CampaignReport.cvs), Float) / cast(func.sum(CampaignReport.clicks), Float)),

        ).group_by(
            AdFee.fee,
            Products.product_name,
        ).filter(
            CampaignReport.promotion_id == Promotion.id,
            Promotion.product_id == Products.id,
            Promotion.media_id == AdMedia.id,
            Promotion.id == AdFee.promotion_id,
            CampaignReport.date.between(start_time, end_time),
        ).order_by(asc(Products.product_name)).all()

        header = [
            'fee',
            'product_name',
            'spend',
            'impressions',
            'clicks',
            'cvs',
            'cpi',
            'ctr',
            'cvr',
        ]

        return header, kpis

    ## for save ##
    @classmethod
    def get_monthly_report_by_product_with_device(cls, start_time=start_time, end_time=end_time):
        session = ads.session

        kpis = session.query(
            CampaignReport.promotion_id,
            label('spend', func.sum(case([(AdFee.fee > 0, CampaignReport.spend * AdFee.fee), ],
                                         else_=CampaignReport.spend / AdFee.fee))),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
        ).group_by(
            CampaignReport.promotion_id,
        ).filter(CampaignReport.date.between(start_time, end_time)).all()

        promotion_schemes = session.query(
            Promotion.id,
            Products.product_name,
            Promotion.device_id,
        ).join(
            Products,
        ).all()

        table = []
        for kpi in kpis:

            cpa = ''
            ctr = ''
            cvr = ''

            # setup cpi
            if kpi[1] == 0 or kpi[4] == 0:
                cpa = 0
            else:
                cpa = int(kpi[1]) / kpi[4]

            # setup ctr
            if kpi[2] == 0 or kpi[3] == 0:
                ctr = 0
            else:
                ctr = kpi[3] / kpi[2]

            # setup cvr
            if kpi[3] == 0 or kpi[4] == 0:
                cvr = 0
            else:
                cvr = kpi[4] / kpi[3]

            __kpi = {
                "promotion_id": kpi[0],
                "spend": int(kpi[1]),
                "impression": int(kpi[2]),
                "clicks": kpi[3],
                "cvs": kpi[4],
                "ctr": ctr,
                "cvr": cvr,
                "cpa": cpa,

            }

            for promotion_scheme in promotion_schemes:
                _promotion_scheme = {
                    "promotion_id": promotion_scheme[0],
                    "name": promotion_scheme[1],
                    "device": promotion_scheme[2],
                }
                if kpi[0] == promotion_scheme[0]:
                    __kpi.update(_promotion_scheme)
                    table.append(__kpi)
        pass

    @classmethod
    def get_report_by_product_with_device(cls, start_time=start_time, end_time=end_time):

        session = ads.session

        kpis = session.query(
            CampaignReport.promotion_id,
            CampaignReport.date,
            label('spend', func.sum(case([(AdFee.fee > 0, CampaignReport.spend * AdFee.fee), ],
                                         else_=CampaignReport.spend / AdFee.fee))),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
        ).group_by(
            CampaignReport.promotion_id,
            CampaignReport.date,
        ).filter(CampaignReport.date.between(start_time, end_time)). \
            order_by(asc(CampaignReport.date)).all()

        promotion_schemes = session.query(
            Promotion.id,
            Products.product_name,
            Promotion.device_id,
        ).join(
            Products,
        ).all()

        table = []
        for kpi in kpis:

            cpa = ''
            ctr = ''
            cvr = ''

            # setup cpi
            if kpi[2] == 0 or kpi[5] == 0:
                cpa = 0
            else:
                cpa = int(kpi[2]) / kpi[5]

            # setup ctr
            if kpi[3] == 0 or kpi[4] == 0:
                ctr = 0
            else:
                ctr = kpi[4] / kpi[3]

            # setup cvr
            if kpi[4] == 0 or kpi[5] == 0:
                cvr = 0
            else:
                cvr = kpi[5] / kpi[4]

            __kpi = {
                "promotion_id": kpi[0],
                "date": kpi[1],
                "spend": int(kpi[2]),
                "impression": kpi[3],
                "clicks": kpi[4],
                "cvs": kpi[5],
                "ctr": ctr,
                "cvr": cvr,
                "cpa": cpa,
            }

            for promotion_scheme in promotion_schemes:
                _promotion_scheme = {
                    "promotion_id": promotion_scheme[0],
                    "name": promotion_scheme[1],
                    "device": promotion_scheme[2],
                }
                if kpi[0] == promotion_scheme[0]:
                    __kpi.update(_promotion_scheme)
                    table.append(__kpi)

        pass

    @classmethod
    def get_report_by_product_with_device(cls, start_time=start_time, end_time=end_time):

        session = ads.session

        kpis = session.query(
            CampaignReport.promotion_id,
            CampaignReport.date,
            label('spend', func.sum(case([(AdFee.fee > 0, CampaignReport.spend * AdFee.fee), ],
                                         else_=CampaignReport.spend / AdFee.fee))),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
        ).group_by(
            CampaignReport.promotion_id,
            CampaignReport.date,
        ).filter(CampaignReport.date.between(start_time, end_time)). \
            order_by(asc(CampaignReport.date)).all()

        # prmotion status
        promotion_schemes = session.query(
            Promotion.id,
            Products.product_name,
            Promotion.device_id,
            # DailyBudget.budget,
            AdFee.fee,
        ).join(
            Products,
        ).all()

        table = []
        for kpi in kpis:

            cpa = ''
            ctr = ''
            cvr = ''

            # setup cpi
            if kpi[2] == 0 or kpi[5] == 0:
                cpa = 0
            else:
                cpa = int(kpi[2]) / kpi[5]

            # setup ctr
            if kpi[3] == 0 or kpi[4] == 0:
                ctr = 0
            else:
                ctr = kpi[4] / kpi[3]

            # setup cvr
            if kpi[4] == 0 or kpi[5] == 0:
                cvr = 0
            else:
                cvr = kpi[5] / kpi[4]

            __kpi = {
                "promotion_id": kpi[0],
                "date": kpi[1],
                "spend": int(kpi[2]),
                "impression": kpi[3],
                "clicks": kpi[4],
                "cvs": kpi[5],
                "ctr": ctr,
                "cvr": cvr,
                "cpa": cpa,
            }

            for promotion_scheme in promotion_schemes:
                _promotion_scheme = {
                    "promotion_id": promotion_scheme[0],
                    "name": promotion_scheme[1],
                    "device": promotion_scheme[2],
                    "fee": promotion_scheme[3],
                }
                if kpi[0] == promotion_scheme[0]:
                    __kpi.update(_promotion_scheme)

                    table.append(__kpi)
        print('<>>>>>>>>>>>>>>>>>')
        print(table)

    @classmethod
    def get_campaign_report_by_days(cls, start_time=start_time, end_time=end_time):

        start_time = start_time.strftime('%Y-%m-%d')
        end_time = end_time.strftime('%Y-%m-%d')

        session = ads.session

        kpis = session.query(
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name,
            label('spend', func.sum(case([(AdFee.fee > 0, CampaignReport.spend * AdFee.fee), ],
                                         else_=CampaignReport.spend / AdFee.fee))),
            label('impressions', func.sum(CampaignReport.impressions)),
            label('clicks', func.sum(CampaignReport.clicks)),
            label('cvs', func.sum(CampaignReport.cvs)),
        ).join(
            Promotion,
            AdMedia
        ).group_by(
            CampaignReport.promotion_id,
            CampaignReport.date,
            AdMedia.media_name
        ).filter(CampaignReport.date.between(start_time, end_time)). \
            order_by(asc(CampaignReport.date)).all()

        promotion_schemes = session.query(
            Promotion.id,
            Products.product_name,
            Promotion.device_id,
        ).join(
            Products,
        ).all()

        table = []
        for kpi in kpis:
            cpi = ''
            ctr = ''
            cvr = ''

            # setup cpi
            if kpi[3] == 0 or kpi[6] == 0:
                cpi = 0

            # setup ctr
            if kpi[5] == 0 or kpi[4] == 0:
                ctr = 0

            # setup cvr
            if kpi[5] == 0 or kpi[6] == 0:
                cvr = 0

            __kpi = {
                "promotion_id": kpi[0],
                "date": kpi[1],
                "media": kpi[2],
                "spend": int(kpi[3]),
                "impression": kpi[4],
                "clicks": kpi[5],
                "cvs": kpi[6],
                "ctr": kpi[5] / kpi[4],
                "cvr": kpi[6] / kpi[5],
                "cpi": kpi[6] / kpi[5],
            }

            for promotion_scheme in promotion_schemes:
                _promotion_scheme = {
                    "promotion_id": promotion_scheme[0],
                    "name": promotion_scheme[1],
                    "device": promotion_scheme[2],
                }
                if kpi[0] == promotion_scheme[0]:
                    __kpi.update(_promotion_scheme)
                    table.append(__kpi)

