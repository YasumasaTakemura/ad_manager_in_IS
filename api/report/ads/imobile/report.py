import os
import pickle
from datetime import datetime, timedelta, time
from db.ads import ads
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from report.scraper.scraper.Scraper import Scraper
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from utils.funcs import *

session = ads.session

class Imobile(Scraper):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self._type_account = kwargs['type_account']

    # set up URLs
    LOGIN_URL = 'https://spagency.i-mobile.co.jp/advertiser.aspx?loginId={}'
    BASE_URL = 'https://spadvertiser.i-mobile.co.jp/'
    SITE_TOP = BASE_URL + 'site.aspx'

    # deprecated
    CAMPAIGN_TOP = BASE_URL + 'campaign.aspx'

    # use this url
    CAMPAIGN_LIST = BASE_URL + 'campaign.aspx?siteId={}'
    CAMPAIGN_MONTHLY_REPORT = BASE_URL + 'campaign_report_monthly=campaign_monthly_report.aspx?campaignId={}'
    CAMPAIGN_DAILY_REPORT = BASE_URL + 'campaign_daily_report.aspx?campaignId={}&begin={}'


    def initialize(self):

        self._params['elements']['id']['username'] = 'ctl00_ContentPlaceHolder2_Login1_UserName'
        self._params['elements']['id']['password'] = 'ctl00_ContentPlaceHolder2_Login1_Password'
        self._params['elements']['id']['submit'] = 'ctl00_ContentPlaceHolder2_Login1_LoginButton'
        self._params['login'] = self.read_files('accounts.json')['account'][0]

    @property
    def dataset(self):
        return self._rows


    @property
    def start_time(self):
        return self._params['time_range']['start_time']

    @start_time.setter
    def start_time(self,start_time):
        self._params['time_range']['start_time'] = start_time

    def set_pkl(self, path, filename):
            file = filename + '.pkl'
            file_path = os.path.join(path, file)
            pickle.dump(self._rows, open(file_path, "wb"))

    def get_pkl(self, path, filename):
            file = filename + '.pkl'
            file_path = os.path.join(path, file)
            self._rows = pickle.load(open(file_path, "rb"))

    # login
    def _login(self, id='id', click='click'):
        try:
            username = self._driver.find_element_by_id(self._params['elements']['id']['username'])
            password = self._driver.find_element_by_id(self._params['elements']['id']['password'])

            username.send_keys(self._params['login']['username'])
            password.send_keys(self._params['login']['password'])

            # input submit or click button to submit
            self.click_id(self._params['elements']['id']['submit'])

        except NoSuchElementException as e:
            self._driver.quit()

    def check_campaign_id(self):
        pass

    # access dashboard page first
    def _go_to_dashboard(self):
        self.go(self.LOGIN_URL.format(self._media_account_id))
        self._login()
        self.go(str(self.SITE_TOP))

    # not necessary
    def _go_to_campaign_top(self):
        self.go(self.CAMPAIGN_TOP)
        self.load_html()
        self._load_campaign_structure()

    # def _go_to_campaign_page(self,campaign_id):
    #     self.go(self.CAMPAIGN_LIST.format(campaign_id))


    # def _get_registered_campaigns(self):
    #     registered_campaigns = []
    #     for id in self._media_campaign_id:
    #         temp ={}
    #         for param in self._params['campaign_structure']:
    #             if id == param['siteId']:
    #                 temp.update(
    #                     {
    #                         'campaign_name': param['site_name'],
    #                         'campaign_id': param['site_id'],
    #                         'adset_name': param['campaign_name'],
    #                         'adset_id': param['campaign_id'],
    #                         'promotion_id': self._promotion_id,
    #
    #                     }
    #                 )
    #                 registered_campaigns.append(temp)
    #                 break
    #     return registered_campaigns

    def __match_campaign_site_name(self,id):
        temp =[]
        for param in self._params['campaign_structure']:
            if param['site_id'] == id:

                temp.append(param)

        return temp


    def _load_each_campaign_report(self):
        for campaign in self._type_account:
            site_camp_ids = self.__match_campaign_site_name(campaign['media_campaign_id'])
            for site_camp_id in site_camp_ids:
                self.go(self.CAMPAIGN_DAILY_REPORT.format(site_camp_id['campaign_id'],self._params['time_range']['start_time']))
                self.load_html()
                self.__export_daily_report(campaign['promotion_id'],**site_camp_id)


    # if self_type equals
    def _load_campaign_structure(self):

        # get elements from 'tr' with this children
        rows = BeautifulSoup(self._data, 'lxml').select('.ListPanel table.List tbody tr')

        for row in rows:
            temp = {}
            try:

                # class name 'Column_Name' has site_id and campaign_id
                for col in row.select('td.Column_Name'):
                    id_type = re.findall(r'[^\s\?\=\&]+', col.a['href'])
                    name = re.findall(r'\S+', col.a.text)[0]

                    # matched site id
                    if id_type[-2] == 'siteId':
                        site_id = id_type[-1]
                        site_name = name
                        temp.update({'site_id': site_id, 'site_name': site_name})

                    # matched campaign id
                    elif id_type[-2] == 'campaignId':
                        campaign_id = id_type[-1]
                        campaign_name = name
                        temp.update({'campaign_id': campaign_id, 'campaign_name': campaign_name})

                    # for a exception
                    else:
                        break

            except Exception as e:
                pass

            self._params['campaign_structure'].append(temp)


    def __export_daily_report(self,id, **kwargs):

        # header
        # has to be in an order and all columns
        header_name = [
            'date',
            'impressions',
            'clicks',
            'ctr',
            'cpc',
            'cvs',
            'cvr',
            'cpa',
            'spend',
        ]

        dataset = []

        rows = BeautifulSoup(self._data, 'lxml').select('.ListPanel table.List tbody tr')

        for row in rows:

            temp = {
                'campaign_name': kwargs['site_name'],
                'campaign_id': kwargs['site_id'],
                'adset_name': kwargs['campaign_name'],
                'adset_id': kwargs['campaign_id'],
                'promotion_id': id,
            }

            for i, (col, header) in enumerate(zip(row.select('td'), header_name)):  # row

                # for casting datetime format
                # datetime shows in a first column
                if i == 0:
                    temp.update({header: date_caster(col.text)})

                else:
                    temp.update({header: num_caster(remove_nt(col.text))})

            dataset.append(temp)

            # remove invalid keys
            invalid_keys = [
                'ctr',
                'cpc',
                'ctr',
                'cvr',
                'cpa', ]

            dataset = remove_specified_key(dataset, invalid_keys)

        # append each campaign dataset
        self._rows += dataset


class CampaignReport(Imobile):
    def export_campaign_report(self):

        self._go_to_dashboard()
        self._go_to_campaign_top()
        # usually load each campaigns already registered
        self._load_each_campaign_report()






