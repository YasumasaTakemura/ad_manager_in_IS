import os
import pickle
import re
import time
from report.scraper import Scraper
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


class Adjust(Scraper):
    def __init__(self):
        super().__init__(self)

    def regex_adjust_c_name(self, text):
        s = re.findall(r"[^\[\]\_]+", text)

        if len(s) == 1:
            return s[0]

        elif len(s) == 2:
            return s[1]

        elif len(s) == 3:
            reg = re.findall(r'[iosiOSandAnd]+' , s[-1])
            if [s[-1]] == reg:
                return s[1]

            _text = s[1]+ '_' +s[-1]
            return _text
        else:
            return


    # for overload
    def parse_table(self):


        ####
        # for test
        ####
        with open('table.pkl', 'rb') as f:
            data = pickle.load(f)

        _data = BeautifulSoup(data, 'lxml')

        # ref each dataset
        headers = _data.select('.s-values .t-head.t-scroll .tr .th sort')
        medias = _data.select('.s-column .tr-container.with-guidelines .tr.tr-body tracker-link')
        values = _data.select('.s-values .tr-container.with-guidelines .tr.tr-body')

        # list up field of media
        media_list = [self.regex_adjust_c_name(media.contents[0]['title'].split(' ')[0]) for media in medias[1:]]

        # list up header
        header_list = [header['column'] for header in headers[1:]]
        # datasets = (dataset.append(self.num_caster(val['title'])) for value in values[1:] for val in value.contents[1:])

        rows = []

        # number of header you need to get
        index_of_header = 8
        for value, media in zip(values[1:], media_list):  # row
            temp = {'media': media,'date':self._params['today']}
            for head, val in zip(header_list[:index_of_header], value.contents[1:][:index_of_header]):  # td
                temp.update({head: self.num_caster(val['title'])})
            rows.append(temp)

        self._data = rows

    def export_data(self):
        self.go(self._params['login']['url'])
        self._wait_until_by_id(val=str(self._params['id']['username']))
        self.login()
        self.set_cookie(os.getcwd(), 'test')
        time.sleep(10)
        self.go(
            'https://next.adjust.com/#/statistics/overview/default/bwc0qgs1axog?sort=installs&reverse=true&timezone_id=172&from=2017-03-15&to=2017-03-15&range=yesterday')
        time.sleep(10)
        # self._wait_until_by_url_change(url=str(self._params['id']['username']))
        # self._wait_until_by_css(val='tr-container.with-guidelines')
        # self._wait_until_by_css(val='main.loaded')
        self.load_html()
        # pickle.dump(self._data, open('table.pkl', "wb"))

        with open('table.pkl', 'wb') as f:
            pickle.dump(self._data, f)

        # self.__wait_until_by_xpath(val='/html/body/div/div/div/div[2]/ul')
        # self.__wait_loading_dashboard()
        print('done!')


    def __wait_loading_dashboard(self):
        self._driver.getAttribute('scroll').contains('apps')


    def login(self, id='id', click=True):
        try:
            username = self._driver.find_element_by_id(self._params['id']['username'])
            password = self._driver.find_element_by_id(self._params['id']['password'])

            username.send_keys(self._params['login']['username'])
            password.send_keys(self._params['login']['password'])

            # input submit or click button to submit
            self.click_xpath('/html/body/div/div/div/div[2]/div/form/div[4]/button')



        except NoSuchElementException as e:
            pass
            # self._driver.quit()
