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


class Resister:
    ##########################################
    # Resister
    ##########################################

    def __init__(self):
        self._account_id = ''
        self._product_id = ''
        self._media_id = ''
        self._device_id = ''

    def resister_promotion(self, **kwargs):

        ## validate empty
        for k, v in kwargs.items():
            if v is '':
                return jsonify(data='invalid')


        ######################################
        #  register new account
        ######################################
        if kwargs['account_id'] == 0:
            account = {'account_name': kwargs['account_name']}

            try:
                ## register
                session.add(AdAccount(**account))
                session.commit()

                ## select
                account_name = session.query(AdAccount).filter(AdAccount.account_name == kwargs['account_name']).first()
                self._account_id = account_name.id

            except SQLAlchemyError as e:
                print(e)
                session.rollback()


        ######################################
        #  register new product
        ######################################
        if kwargs['product_id'] == 0:

            # 2nd resister product
            product = {
                'product_name': kwargs['product_name'],
                'account_id': self._account_id
            }

            print('>>>>>>>>>>>>>>>>>>>')
            print(product)

            try:
                ## register
                session.add(Products(**product))
                session.commit()

                ## select
                product_name = session.query(Products).filter(Products.product_name == kwargs['product_name'],
                                                              Products.account_id == self._account_id).first()
                self._product_id = product_name.id

            except SQLAlchemyError as e:
                print(e)
                session.rollback()


        ######################################
        #  if accounts and products is already existed
        ######################################

        # 1st resister account
        try:
            self._account_id = session.query(AdAccount.id).filter(AdAccount.id == kwargs['account_id']).first()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()

        # 2nd resister product

        try:
            self._product_id = session.query(Products.id).filter(Products.id == kwargs['product_id']).first()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()

        # 3rd  resister promotion
        try:

            promotion = {
                'account_id': self._account_id,
                'product_id': self._product_id,
                'media_id': kwargs['media_id'],
                'device_id': kwargs['device_id'],
            }

            session.add(Promotion(**promotion))
            session.commit()

            promotion_id = session.query(Promotion.id).filter(
                Promotion.account_id == self._account_id,
                Promotion.product_id == self._product_id,
                Promotion.media_id == kwargs['media_id'],
                Promotion.device_id == kwargs['device_id'],
            ).first()

            return promotion_id

        except SQLAlchemyError as e:
            print(e)
            session.rollback()


    def resister_ad_account(self, name):

        _name = {'account_name': name}

        try:
            session.add(AdAccount(**_name))
            session.commit()
            account_name = session.query(AdAccount).filter(AdAccount.account_name == _name['account_name']).first()
            self._account_id = account_name.id
            return self._account_id

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_media(self, name):

        _name = {'media_name': name}

        try:
            session.add(AdMedia(**_name))
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_products(self, id, name):

        _name = {
            'account_id': id,
            'product_name': name
        }

        try:
            session.add(Products(**_name))
            session.commit()
            product = session.query(Products).filter(Products.product_name == _name['product_name']).one()
            return product.id


        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_fee(self, **kwargs):

        p_id = kwargs.get('id', False)
        fee = kwargs.get('fee', 1.0)

        print(p_id)
        print(fee)

        # empty is not allowed
        if p_id is False:
            print('something is empty')
            return False

        _fee = {
            'promotion_id': p_id,
            'fee': fee,
        }

        try:
            session.add(AdFee(**_fee))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_daily_budget(self, **kwargs):
        p_id = kwargs.get('id', False)
        annually = kwargs.get('annually', False)
        monthly = kwargs.get('monthly', False)
        daily = kwargs.get('daily', False)
        at = kwargs.get('at', False)
        start = kwargs.get('start', False)
        end = kwargs.get('end', False)

        _budget = {
            'promotion_id': p_id,
        }

        if not annually and not monthly and not daily:
            print('you have to set at least one col from "annually" "monthly" "daily" ')

        # empty is not allowed
        if '' in [p_id, annually, monthly, daily, at, start, end, ]:
            print('something is empty')
            return False

        try:
            # validate period
            # has to be set at least at or start-end
            if not at and not start:
                # print('you have to set "at" or "start-end"')

                if annually:
                    _budget.update({'annually': annually})

                elif monthly:
                    _budget.update({'monthly': monthly})

                elif daily:
                    _budget.update({'daily': daily})

                session.add(DailyBudget(**_budget))
                session.commit()

            else:
                # type must to be string
                if at:
                    print('here')
                    _budget.update({'at': datetime.strptime(at, '%Y-%m-%d')})

                # type must to be string
                elif not end:
                    _budget.update({'start': datetime.strptime(start, '%Y-%m-%d'), 'end': end_of_month(1)})

                else:
                    _budget.update(
                        {'start': datetime.strptime(start, '%Y-%m-%d'), 'end': datetime.strptime(end, '%Y-%m-%d')})

                session.add(DailyBudget(**_budget))
                session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    # def resister_monthly_budget(self, **kwargs):
    #     p_id = kwargs.get('id', False)
    #     annually = kwargs.get('annually', False)
    #     monthly = kwargs.get('monthly', False)
    #     daily = kwargs.get('daily', False)
    #     at = kwargs.get('at', False)
    #     start = kwargs.get('start', False)
    #     end = kwargs.get('end', False)
    #
    #     _budget = {
    #         'promotion_id': p_id,
    #     }
    #
    #     if not annually and not monthly and not daily:
    #         print('you have to set at least one col from "annually" "monthly" "daily" ')
    #
    #     # empty is not allowed
    #     if '' in [p_id, annually, monthly, daily, at, start, end, ]:
    #         print('something is empty')
    #         return False
    #
    #     try:
    #         # validate period
    #         # has to be set at least at or start-end
    #         if not at and not start:
    #             # print('you have to set "at" or "start-end"')
    #
    #             if annually:
    #                 _budget.update({'annually': annually})
    #
    #             elif monthly:
    #                 _budget.update({'monthly': monthly})
    #
    #             elif daily:
    #                 _budget.update({'daily': daily})
    #
    #             session.add(DailyBudget(**_budget))
    #             session.commit()
    #
    #         else:
    #             # type must to be string
    #             if at:
    #                 print('here')
    #                 _budget.update({'at': datetime.strptime(at, '%Y-%m-%d')})
    #
    #             # type must to be string
    #             elif not end:
    #                 _budget.update({'start': datetime.strptime(start, '%Y-%m-%d'), 'end': end_of_month(1)})
    #
    #             else:
    #                 _budget.update(
    #                     {'start': datetime.strptime(start, '%Y-%m-%d'), 'end': datetime.strptime(end, '%Y-%m-%d')})
    #
    #             session.add(DailyBudget(**_budget))
    #             session.commit()
    #
    #     except SQLAlchemyError as e:
    #         print(e)
    #         session.rollback()
    #         pass

    def resister_monthly_budget(self, **kwargs):
        p_id = kwargs.get('id', False)

        print(p_id)

        # empty is not allowed
        if p_id is False:
            print('something is empty')
            return False

        _budget = {
            'promotion_id': p_id,
        }

        try:
            session.add(MonthlyBudget(**_budget))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_staff(self, **kwargs):
        p_id = kwargs.get('id', False)

        print(p_id)

        # empty is not allowed
        if p_id is False:
            print('something is empty')
            return False

        _staff = {
            'promotion_id': p_id,
        }

        try:
            session.add(Staff(**_staff))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_istool(self, **kwargs):
        p_id = kwargs.get('id', False)
        # empty is not allowed
        if p_id is False:
            print('something is empty')
            return False

        try:
            session.add(Istool(**{'promotion_id': p_id, }))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_report_manager(self, **kwargs):
        session = ads.session

        p_id = kwargs.get('id', False)
        media_account_id = kwargs.get('media_account_id', False)
        media_campaign_id = kwargs.get('media_campaign_id', False)

        if media_campaign_id is False:

            _promotion_id = {
                'promotion_id': kwargs['promotion_id'],
                'media_account_id': kwargs['media_account_id'], }
        else:
            _promotion_id = {
                'promotion_id': kwargs['promotion_id'],
                'media_account_id': kwargs['media_account_id'],
                'media_campaign_id': kwargs['media_campaign_id'],
            }

        try:
            session.add(AdReportManager(**_promotion_id))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass
