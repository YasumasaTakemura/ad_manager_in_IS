from datetime import *
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from sqlalchemy import asc, desc
from db.ads.ads import CampaignReport,Products,AdMedia,session
import pickle
import os
import json
import re
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.funcs import *

# bind ads connection

class Scraper:

    ###########################
    # ChromeDriver config
    ###########################
    chromeOptions = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '/app'}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument(
        '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')
    driver_path = '/Users/YasumasaTakemura/Downloads/chromedriver'

    def __init__(self,**kwargs):
        self.ip_address = []
        self._media_account_id = kwargs['media_account_id']
        self._type_account = kwargs['type_account']
        # self._media_campaign_ids = []
        # self._promotion_id = kwargs['promotion_id']
        self._type = kwargs['type']

        # selenium
        self._params = {}
        self.browser = 'Chrome'
        self._driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=self.chromeOptions)
        self._data = []
        self._rows = []
        self._current_url = None
        self._past_url = None
        self._urls = []
        self.t = CampaignReport
        self.media = ''
        self._params = {
            'url': '',
            'urls': [],
            'ip_address': '',
            'account': {
                'service_name': '',
                'media': '',

            },
            # for campaign_structure
            # to set campaign id , adset id and ...
            'campaign_structure': [],
            'elements': {
                'id': {
                    'username': '',
                    'password': '',
                },
            },
            'login': {
                'username': '',
                'password': '',
                'submit': '',

            },
            'time_range': {
                'start_time': '2017-03-01',
                'end_time': '2017-03-14',
            },
            'today': datetime.now().strftime('%Y-%m-%d')
        }

    # for overload
    def initialize(self):
        pass

    # load json files for account information
    def read_files(self, filename):
        this_dir = os.path.dirname(__file__)
        _filename = os.path.join(this_dir, filename)
        path = os.path.join(this_dir, filename)
        with open(_filename) as k:
            keys = json.load(k)
        return keys


    # get html and put into _data
    def load_html(self):
        self._data = self._driver.page_source

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, urls):
        self._urls = urls


    def update_input_params(self, params, key):
        try:
            if key == 'xpath':
                if isinstance(params, dict):
                    self._params['xpath'].update(params)

                elif isinstance(params, list):
                    for param in params:
                        self._params['xpath'].update(param)

                else:
                    raise TypeError()

            elif key == 'username':
                self._params['username'] = params['username']

            elif key == 'password':
                self._params['password'] = params['password']

            else:
                self._params.update(params)

        except Exception as e:
            print(e)

    ##########################################
    # Validator
    ##########################################
    def _validate_elements(self):
        pass

    ##########################################
    # Cookie
    ##########################################
    def set_cookie(self, path, filename):
        file = filename + '.pkl'
        file_path = os.path.join(path, file)
        pickle.dump(self._driver.get_cookies(), open(file_path, "wb"))

    def get_cookie(self, path, filename):
        file = filename + '.pkl'
        file_path = os.path.join(path, file)
        cookies = pickle.load(open(file_path, "rb"))
        print(cookies)
        for cookie in cookies:
            self._driver.add_cookie(cookie)

    ##########################################
    # Waiter
    ##########################################
    def wait_until_redirected(self, index, timer=3, ):
        wait = WebDriverWait(self._driver, timer)
        wait.until(lambda driver: driver.current_url != str(self._params['url'][index]))

    def _wait_until_by_url_change(self, sleep=30, url=None):
        if url:
            WebDriverWait(self._driver, sleep).until(lambda driver: driver.current_url != url)

        else:
            WebDriverWait(self._driver, sleep).until(lambda driver: driver.current_url != self._past_url)

    def _wait_until_by_id(self, sleep=30, val=None):
        WebDriverWait(self._driver, sleep).until(EC.presence_of_element_located((By.ID, val)))

    def _wait_until_by_xpath(self, sleep=30, val=None):
        WebDriverWait(self._driver, sleep).until(EC.presence_of_element_located((By.XPATH, val)))

    def _wait_until_by_type(self, sleep=30, val=None):
        WebDriverWait(self._driver, sleep).until(EC.presence_of_element_located((By.XPATH, val)))

    def _wait_until_by_css(self, sleep=30, val=None):
        WebDriverWait(self._driver, sleep).until(EC.presence_of_element_located((By.CSS_SELECTOR, val)))

    ##########################################
    # Login
    ##########################################
    def login(self, id='id', click='click'):
        pass
        # try:
        #     if id == 'id':
        #         username = self._driver.find_element_by_id(self._params['id']['username'])
        #         password = self._driver.find_element_by_id(self._params['id']['password'])
        #
        #     elif id == 'class':
        #         username = self._driver.find_element_by_class_name(self._params['class']['username'])
        #         password = self._driver.find_element_by_class_name(self._params['class']['password'])
        #
        #     else:
        #         username = self._driver.find_element_by_xpath(self._params['xpath']['username'])
        #         password = self._driver.find_element_by_xpath(self._params['xpath']['password'])
        #
        #     username.send_keys(self._params['login']['username'])
        #     password.send_keys(self._params['login']['password'])
        #
        #     # input submit or click button to submit
        #     if click == 'click':
        #         # submit
        #         self.click_id(self._params['login']['submit'])
        #     else:
        #         password.submit()
        #
        #         # print(password.is_displayed())
        #         # print(username.is_displayed())


        # except NoSuchElementException as e:
        #     print(e)
        #     self._driver.quit()

    ##########################################
    # ScreenShot
    ##########################################
    def ss(self, filename='username {}.jpg'.format(datetime.now())):
        self._driver.save_screenshot(filename)

    ##########################################
    # Clicks
    ##########################################
    def click_id(self, val):
        self._driver.find_element_by_id(val).click()

    def click_class(self, val):
        self._driver.find_element_by_class_name(val).click()

    def click_text_link(self, val):
        self._driver.find_element_by_link_text(val).click()

    def click_xpath(self, val):
        self._driver.find_element_by_xpath(val).click()

    def quite(self):
        self._driver.quit()

    ##########################################
    # Redirect
    ##########################################
    def go(self, url):
        self._past_url = self._current_url
        self._driver.get(url)
        self._current_url = str(url)

    def go_until(self, url):

        if self._past_url is None:
            self.go(url)

        else:
            self._past_url = self._current_url
            self._driver.get(url)
            self._current_url = str(url)
            self._wait_until_by_url_change()


    def resume(self):
        for i, url in enumerate(self._params['urls']):
            if self._past_url == str(url):
                self.go_until(str(self._params['urls'][i + 1:]))

    def redirect_all(self, resume=False, stop=None, action=None, args=None, start=None, end=None):

        # stop redirect and do some action
        if self._driver.current_url == str(stop):
            action(args)

        # redirect both are set
        elif start or end:
            for url in self._urls[start:end]:
                self.go_until(str(url))

        # redirect only start is set
        elif start and not end:
            self.go_until(str(self._urls[start:]))

        # redirect only end is set
        elif end and not start:
            self.go_until(str(self._urls[:end]))

        # redirect all
        else:
            for url in self._urls:
                self.go_until(str(url))

    # for overload
    def parse_table(self):
        pass

    ##########################################
    # Database
    ##########################################

    def get_services(self,name):
        try:
            t = Products
            data = session.query(t).filter(t.service_name == name).all()
            session.close()
            return parseSAtoJson(data)
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()

    def get_media(self,name):
        try:
            t = Products
            data = session.query(t).filter(t.service_name == name).all()
            session.close()
            return parseSAtoJson(data)
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()

    def get_account(self,name):
        try:
            t = Products
            data = session.query(t).filter(t.service_name == name).all()
            session.close()
            return parseSAtoJson(data)
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            session.close()

    def select(self, date=None, account=None, title=None, media=None, ):
        data = session.query(self.t).filter(self.t.date == date, self.t.company_name == account, self.t.service_name == title,
                                    self.t.media == media).all()
        session.close()
        return parseSAtoJson(data)

    def to_csv(self, filename):
        header = list(self._rows[0].keys())
        json_to_csv(self._rows, header, filename)

    def insert(self):
        for row in self._rows:
            try:
                session.add(self.t(**row))
                session.commit()

            except SQLAlchemyError as e:
                print(e)
                session.rollback()
                pass
        session.close()

    def insert_all(self):

        try:
            session.add_all(self.t(self._rows))
            session.commit()

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            pass

        session.close()
        
    def upsert_campaign_report(self):

        for row in self._rows:

            # check not duplicated
            res = session.query(CampaignReport).filter(CampaignReport.date == row['date'],
                                                 CampaignReport.campaign_id == row['campaign_id'],
                                                 CampaignReport.adset_id == row['adset_id'])

            # INSERT new data
            if not res.first():

                try:
                    session.add(CampaignReport(**row))
                    session.commit()

                except IntegrityError as e:
                    session.rollback()


                except SQLAlchemyError as e:
                    print(e)
                    session.rollback()
                    pass

            # UPDATE existing date
            try:

                res.update(row)
                session.commit()

            except SQLAlchemyError as e:
                print(e)
                session.rollback()
                pass

        session.close()
