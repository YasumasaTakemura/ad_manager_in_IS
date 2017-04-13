from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from report.scraper.scraper.Scraper import Scraper
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from utils.funcs import *
import random
import time as timer


class Nend(Scraper):

    # set up URLs
    LOGIN_URL = 'https://www.nend.net/admin/login'
    BASE_URL = 'https://www.nend.net/d/'
    AdvertiserPage = BASE_URL + 'advertiser/login/{}'
    HomeDashboard = BASE_URL + 'home'
    PromotionPage = BASE_URL + 'promotion'
    CampaignPage = BASE_URL + 'campaign/index?advertiser_id={}&advertiser_promotion_id={}'
    CAMPAIGN_REPORT = BASE_URL + 'report/search?advertiser_id={}&advertiser_campaign_id={}&advertiser_promotion_id={}'

    def initialize(self):
        self._params['elements']['id']['username'] = 'UserMail'
        self._params['elements']['id']['password'] = 'UserPass'
        self._params['elements']['id']['submit'] = ''
        self._params['login'] = self.read_files('accounts.json')['account'][1]

    @property
    def dataset(self):
        return self._rows

    @property
    def start_time(self):
        return self._params['time_range']['start_time']

    @start_time.setter
    def start_time(self, start_time):
        self._params['time_range']['start_time'] = start_time


    # login
    # recommended to implement by each classes
    def _login(self, id='id', click='click'):
        try:
            username = self._driver.find_element_by_id(self._params['elements']['id']['username'])
            password = self._driver.find_element_by_id(self._params['elements']['id']['password'])

            username.send_keys(self._params['login']['username'])
            password.send_keys(self._params['login']['password'])

            # input submit or click button to submit
            password.submit()

            # wait for redirecting
            timer.sleep(2)

        except NoSuchElementException as e:
            self._driver.quit()

    def check_campaign_id(self):
        pass

    # access dashboard page first
    def _go_to_dashboard(self):
        self.go(self.LOGIN_URL)
        self._login()
        self.go(self.AdvertiserPage.format(self._media_account_id))
        timer.sleep(3)
        self.go(self.HomeDashboard)

    def __match_campaign_site_name(self, id):
        temp = []
        for param in self._params['campaign_structure']:
            if param['site_id'] == id:
                temp.append(param)

        return temp

    def _load_structures(self):
        self.__load_campaign_structure()

    # get structure of promotion level
    def __load_promotion_structure(self):
        self.go(self.PromotionPage)
        self.load_html()

        rows = BeautifulSoup(self._data, 'lxml').select('.info.html5jp-tbldeco tbody tr')

        campaign_structure = []

        for row in rows:
            try:

                # class name 'name' has campaign name  and campaign_id
                for col in row.select('td.name p '):
                    id = re.findall(r'[^\s\?\=\&\/]+', col.a['href'])
                    name = re.findall(r'\S+', col.a.text)[0]

                    campaign_id = id[-1]
                    campaign_name = name

                    # match promotion_id and promotion id of nend
                    promotion_id =''
                    for type in self._type_account:
                        if detect_device_type(name.split('_')[-1].lower()) == type['device']:
                            promotion_id = type['promotion_id']

                    campaign_structure.append(
                        {'promotion_id': promotion_id, 'campaign_id': campaign_id, 'campaign_name': campaign_name})

            except Exception as e:
                pass
        return campaign_structure

    # if self_type equals
    def __load_campaign_structure(self):

        campaign_structure = self.__load_promotion_structure()

        # get structure of campaign level
        for structure in campaign_structure:

            self.go(self.CampaignPage.format(self._media_account_id, structure['campaign_id']))
            self.load_html()

            # get elements from 'tr' with this children
            rows = BeautifulSoup(self._data, 'lxml').select('.info.html5jp-tbldeco tbody tr')

            for row in rows:
                try:

                    # class name 'name' has campaign name  and campaign_id
                    for col in row.select('td.name p '):
                        id = re.findall(r'[^\s\?\=\&\/]+', col.a['href'])
                        name = re.findall(r'\S+', col.a.text)[0]

                        adset_id = id[-1]
                        adset_name = name

                        structure.update({'adset_id': adset_id, 'adset_name': adset_name})


                except Exception as e:
                    pass

                self._params['campaign_structure'].append(structure)


    def _load_each_campaign_report(self):
        for campaign in self._params['campaign_structure']:
            self.go(str(self.CAMPAIGN_REPORT.format(self._media_account_id,
                                                    campaign['adset_id'],
                                                    campaign['campaign_id'],
                                                    )))
            self.load_html()
            self.__export_daily_report(campaign)


    def __export_daily_report(self, campaign):
        # header
        # has to be in an order and all columns
        header_name = [
            'date',
            'impressions',
            'clicks',
            'ctr',
            'cpc',
            '__',
            'cvs',
            'cvr',
            'cpa',
            'spend',
        ]

        dataset = []

        rows = BeautifulSoup(self._data, 'lxml', from_encoding='utf-8').select(
            '.info.html5jp-tbldeco.multi-cv-report tbody tr')

        for row in rows:
            try:
                for i, (col, header) in enumerate(zip(row.select('td'), header_name)):  # row

                    # for casting datetime format
                    # datetime shows in a first column
                    if i == 0:
                        campaign.update({header: date_caster(col.text)})

                    elif i in[5,6,7,8]:
                        campaign.update({header: col.div.text})

                    else:
                        campaign.update({header: num_caster(col.text)})

                dataset.append(campaign)

                # remove invalid keys
                invalid_keys = [
                    'ctr',
                    'cpc',
                    'ctr',
                    'cvr',
                    'cpa',
                    '__', ]

                dataset = remove_specified_key(dataset, invalid_keys)
            except Exception as e:
                print(e)

            # append each campaign dataset
            self._rows += dataset


class CampaignReport(Nend):
    def export_campaign_report(self):
        self._go_to_dashboard()
        self._load_structures()
        self._load_each_campaign_report()
        # self.set_pkl(os.getcwd(), 'dataset')

        # if type is "account" load campaign_structure ,
        #  which means load all campaigns including old campaign have already stopped

        # if len(self._type_account) == 0:
        #     for account in self._params['campaign_structure']:
        #         self.go(self.CAMPAIGN_DAILY_REPORT.format(account['campaign_id'],
        #                                                   self._params['time_range']['start_time']))
        #         self.load_html()
        #
        #         self._export_daily_report(**account)
