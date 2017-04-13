import re
from bs4 import BeautifulSoup
from utils.funcs import *

class TableParser:
    def __init__(self):
        self._datasets = []
        self._datasets_to_render = []
        self._header = []
        self._account_info = {'media': ''}
        self._params = {}
        self._invalid_keys = [
            'ctr',
            'cpc',
            'ctr',
            'cvr',
            'cpa', ]

    def setup(self):
        self._header = [self._params['header']]

    @property
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, datasets):
        self._datasets = datasets

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def invalid_keys(self):
        return self._invalid_keys

    @invalid_keys.setter
    def invalid_keys(self, invalid_keys):
        self._invalid_keys = invalid_keys


class Common(TableParser):
    _datasets = []
    _datasets_to_render = []
    _header = []
    _account_info = {}
    _invalid_keys = [
            'ctr',
            'cpc',
            'ctr',
            'cvr',
            'cpa', ]

    @classmethod
    def parser(cls, **kwargs):

        dataset = []

        rows = BeautifulSoup(cls._datasets, 'lxml', from_encoding='utf-8').select('table tr')

        for row in rows:

            temp = {
                'media': cls._account_info['media'],
                'campaign_name': kwargs['site_name'],
                'campaign_id': kwargs['site_id'],
                'adset_name': kwargs['campaign_name'],
                'adset_id': kwargs['campaign_id'],

            }
            for i, (col, header) in enumerate(zip(row.select('td'), cls._header)):  # row

                # for casting datetime format
                # datetime shows in a first column
                if i == 0:
                    temp.update({header: date_caster(col.text)})

                else:
                    temp.update({header: num_caster(remove_nt(col.text))})

            dataset.append(temp)

            dataset = remove_specified_key(dataset, cls._invalid_keys)

        cls._datasets_to_render.append(dataset)
