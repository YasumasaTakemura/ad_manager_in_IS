from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, asc, case
from sqlalchemy.sql import label
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from report.scraper.scraper.Scraper import Scraper
from db.ads.ads import  Products, AdMedia, AdAccount, AdReportManager, AdjustEvents, CampaignReport, \
    DailyBudget,MonthlyBudget, AdFee, Promotion,Device
from db.ads import ads
from db.ads.ads import find_account_name, find_account_id, find_media_id, find_media_name, find_product_id, \
    find_product_name
from utils.funcs import parseSAtoJson, json_to_csv, end_of_month, begging_of_month, today,remove_specified_key
from datetime import datetime
from dateutil.relativedelta import relativedelta
from report.ads.Manager.manager import AdAPItManager


class Manager:




    ## get all reporting task
    @classmethod
    def queue_all_tasks(cls):
        session = ads.session

        all_tasks = session.query(AdReportManager,Promotion,Device).\
            filter(
            AdReportManager.promotion_id == Promotion.id,
            Promotion.device_id == Device.id,
            AdReportManager.reporting == True
        ).all()

        fb = []
        tw = []
        adw = []
        im = []
        nend = []
        yh = []

        tw_id = ''
        im_id=''
        nend_id=''

        print('LENGGH')
        print(len(all_tasks))
        for i,all_task in enumerate(all_tasks):
            print('>>>>>>>>>>>>>>>>>>>>>>>')
            print(len(all_task))
            print(all_task)
            print(i)
            items = {
                'media_account_id': all_task.AdReportManager.media_account_id,
                'type': all_task.AdReportManager.type,
                'type_account':[]
            }

            # add campaign field if type is "campaign"
            if all_task.AdReportManager.type == 'campaign':
                items.update({'media_campaign_id': all_task.AdReportManager.media_campaign_id})

            # i-mobile
            if all_task.Promotion.media_id == 1:
                try:
                    if im_id != all_task.AdReportManager.media_account_id:
                        items['type_account'].append({'media_campaign_id': all_task.AdReportManager.media_campaign_id, 'promotion_id': all_task.Promotion.id})
                        im.append(items)

                    # last obj has same tw_id  so pick up last one as [-1]
                    else:
                        im[-1]['type_account'].append({'media_campaign_id': all_task.AdReportManager.media_campaign_id, 'promotion_id':all_task.Promotion.id})

                    # set for avoiding duplication
                    im_id = all_task.AdReportManager.media_account_id

                except IndexError as e:
                    print(e)
                    pass

            # twitter
            elif all_task.Promotion.media_id == 2:
                try:

                    if tw_id != all_task.AdReportManager.media_account_id:
                        items['type_account'].append({'device': all_task.Device.device, 'promotion_id': all_task.Promotion.id})
                        tw.append(items)

                    # last obj has same tw_id  so pick up last one as [-1]
                    else:
                        tw[-1]['type_account'].append({'device': all_task.Device.device, 'promotion_id': all_task.Promotion.id})
                    tw_id = all_task.AdReportManager.media_account_id

                except IndexError as e:
                    print(e)
                    pass

            # facebook
            elif all_task.Promotion.media_id == 3:
                items.update({'promotion_id': all_task.Promotion.id, })
                fb.append(items)

            # nend
            elif all_task.Promotion.media_id == 4:
                try:
                    if nend_id != all_task.AdReportManager.media_account_id:
                        items['type_accountAdReportManager'].append({'device': all_task.Device.device,'media_campaign_id': all_task.AdReportManager.media_campaign_id, 'promotion_id': all_task.Promotion.id})
                        nend.append(items)

                    # last obj has same tw_id  so pick up last one as [-1]
                    else:
                        nend[-1]['type_account'].append({'device': all_task.Device.device,'media_campaign_id': all_task.AdReportManager.media_campaign_id, 'promotion_id': all_task.Promotion.id})

                    # set for avoiding duplication
                    nend_id = all_task.AdReportManager.media_account_id

                except IndexError as e:
                    print(e)
                    pass


        return im, tw, fb , nend



    @classmethod
    def select_campaign_report_all(cls):
        session = ads.session
        accounts = session.query(AdAccount).join(Promotion).all()
        services = session.query(Products).join(Promotion).all()
        medias = session.query(AdMedia).join(Promotion).all()

        datasets = session.query(Promotion).join(AdAccount, Products, AdMedia).all()

        for dataset in datasets:
            print('>>>>>>>>>>>>')
            print(
                dataset.id,
                dataset.promotion,
                dataset.AdAccount.account_name,
                dataset.Products.product_name,
                dataset.AdMedia.media_name,

            )

            # for result in results:
            #     for res in result:
            #         print(res)

    def join_ad_fee(self):
        pass


class Resister:
    ##########################################
    # Resister
    ##########################################

    def __init__(self):
        self._account_id = ''

    def resister_ad_account(self, name):
        session = ads.session

        _name = {'account_name': name}

        try:
            session.add(AdAccount(**_name))
            session.commit()
            account_name = session.query(AdAccount).filter(AdAccount.account_name == _name['account_name']).one()
            self._account_id = account_name.id

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_media(self, name):
        session = ads.session

        _name = {'media_name': name}

        try:
            session.add(AdMedia(**_name))
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_products(self, id, name):
        session = ads.session

        _name = {
            'account_id': id,
            'product_name': name
        }

        try:
            session.add(Products(**_name))
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_fee(self, **kwargs):
        session = ads.session
        p_id = kwargs.get('id', False)
        fee = kwargs.get('fee', 1.0)

        # empty is not allowed
        if p_id == '':
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
        session = ads.session
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

    def resister_promotion(self, **kwargs):
        session = ads.session

        a_id = kwargs.get('account_id', False)
        p_id = kwargs.get('product_id', False)
        m_id = kwargs.get('media_id', False)
        device = kwargs.get('device', False)
        promotion_id = kwargs.get('promotion_id', False)

        # empty is not allowed
        if '' in [a_id, p_id, m_id, device, promotion_id]:
            print('something is empty')
            ValueError()

        _promotion = {
            'account_id': a_id,
            'product_id': p_id,
            'media_id': m_id,
            'device': device,
        }

        try:
            session.add(Promotion(**_promotion))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    def resister_ad_report_manager(self, **kwargs):
        session = ads.session

        p_id = kwargs.get('promotion_id', False)
        media_account_id = kwargs.get('media_account_id', False)
        media_campaign_id = kwargs.get('media_campaign_id', False)

        _promotion_id = {
            'promotion_id': p_id,
            'media_account_id': media_account_id,
            'media_campaign_id': media_campaign_id,
        }

        try:
            session.add(AdReportManager(**_promotion_id))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

    ##########################################
    # Update
    ##########################################

    def update_ad_account(self, id, name):
        session = ads.session

        try:
            target = session.query(AdAccount).filter(AdAccount.id == id).first()
            target.account_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    def update_ad_media(self, id, name):
        session = ads.session

        try:
            target = session.query(AdMedia).filter(AdMedia.id == id).first()
            target.media_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    def update_products(self, id, name):
        session = ads.session

        try:
            target = session.query(Products).filter(Products.id == id).first()
            target.product_name = name
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    def update_ad_fee(self, id, **kwargs):
        session = ads.session

        try:
            target = session.query(AdFee).filter(AdFee.id == id).first()

            _target = kwargs.get('target', False)
            _fee = kwargs.get('fee', False)

            if target:
                target.tarfet = _target

            target.fee = _fee
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    def update_ad_budget(self, id, **kwargs):
        session = ads.session

        _budget = kwargs.get('_budget')

        try:
            target = session.query(DailyBudget).filter(DailyBudget.id == id).first()

            if _budget:
                target.budget = _budget

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    #
    # def update_media(self, id, name):
    #     try:
    #         target = session.query(Promotion).filter(Promotion.id == id).first()
    #         target.promotion_id = name
    #         session.commit()
    #     except SQLAlchemyError as e:
    #         session.rollback()
    #         

    def update_ad_report_manager(self, id, reporting, media_campaign_id=None):
        session = ads.session

        res = session.query(AdReportManager.media_campaign_id).filter(AdReportManager.id == id).first()

        try:
            res.reporting = reporting

            if not res and media_campaign_id:
                res.media_campaign_id = media_campaign_id

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()


class Manipulator:
    def __init__(self):
        self._result = []

    def get_media_name(self):
        session = ads.session
        medias = []

        results = session.query(
            Promotion
        ).join(AdMedia, Products).all()

        for result in results:
            medias.append((result.id, result.product_id, result.Products.id, result.Products.product_name,
                           result.AdMedia.media_name))

        return medias

    def sum_by_campaign(self):
        session = ads.session

        media_ids_names = self.get_media_name()
        joined = []
        campaigns = session.query(
            CampaignReport.promotion_id,
            CampaignReport.date,
            CampaignReport.device,
            label('spend', func.sum(CampaignReport.spend)),
            label('cvs', func.sum(CampaignReport.cvs)),
        ).join(Promotion, AdMedia).filter(CampaignReport.date == '2017-03-20').group_by(
            CampaignReport.date, CampaignReport.promotion_id, CampaignReport.device,
        ).order_by(asc(CampaignReport.promotion_id)).all()

        for i, campaign in enumerate(campaigns):
            try:
                for id_name in media_ids_names:
                    print('>>>>>>>>>>>>')
                    print(campaign)
                    print(id_name)
                    if campaign[0] == id_name[0]:
                        joined.append({
                            'id': media_ids_names[0],
                            'date': campaign[0],
                            'media': campaign[1],
                            'device': campaign[2],
                            'spend': campaign[3],
                            'cvs': campaign[4],
                            'cpi': campaign[3] / campaign[4],

                        })

            except ZeroDivisionError:
                pass


    def sum_by_campaigns(self):
        session = ads.session
        t = CampaignReport

        result = session.query(
            AdMedia.media_name,
            t.date,
            t.promotion_id,
            t.campaign_name,
            func.sum(t.spend),
            'cvs', func.sum(t.cvs),
            label('impressions', func.sum(t.impressions)),
            label('clicks', func.sum(t.clicks)),
        ).join(Promotion).filter(t.date == '2017-03-20').group_by(
            AdMedia.media_name,
            t.date,
            t.promotion_id,
            t.campaign_name,
            t.spend,
            t.cvs,
            # t.impressions,
            # t.clicks,

        ).order_by(asc(t.date)).all()

        self._result = result

    def shape_group_by(self):
        session = ads.session
        rows = []
        for res in self._result:
            print('>>>>>>>>>>>>>')
            if res.spend > 0:
                row = {
                    'date': res.date,
                    'campaign_name': res.campaign_name,
                    'spend': res.spend,
                    'cvs': res.cvs,
                    'cpi': int(res.spend / res.cvs),
                    'cpc': int(res.spend / res.clicks),
                    'impressions': res.impressions,
                    'clicks': res.clicks,
                    # 'media':res[0].media_name,
                    'media2': res,
                }
                rows.append(row)
            else:
                row = {
                    'date': res.date,
                    'campaign_name': res.campaign_name,
                    'spend': res.spend,
                    'cvs': res.cvs,
                    'cpi': 0,
                    'impressions': res.impressions,
                    'clicks': res.clicks,
                    # 'media':res[0].media_name,
                    'media2': res,
                }
                rows.append(row)
        return rows


class Get:

    def get_accounts(self):
        session = ads.session
        accounts = session.query(AdAccount).order_by(asc(AdAccount.id)).all()
        for account in accounts:
            act = {
                'id': account.id,
                'account_name': account.account_name
            }
            print(act)

    def get_products(self):
        session = ads.session
        products = session.query(Products).order_by(asc(Products.id)).all()
        for product in products:
            act = {
                'id': product.id,
                'product_name': product.product_name,
                'account_is': product.AdAccount.id,
                'account_name': product.AdAccount.account_name,

            }
            print(act)

    def get_promotions(self):
        session = ads.session
        promotions = session.query(Promotion).order_by(asc(Promotion.id)).all()
        for promotion in promotions:
            pr = {
                'id': promotion.id,
                'media_name': promotion.AdMedia.media_name,
                'product_name': promotion.Products.product_name,
                'account_name': promotion.AdAccount.account_name,
                'device': promotion.device,
            }
            for report in promotion.AdReportManager:
                pr.update({'reporting': report.reporting})
                # print(report.reporting)
            print(pr)
