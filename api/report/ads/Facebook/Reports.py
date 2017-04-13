from facebookads.objects import AdAccount, AsyncJob, adsinsights, AdImage, AdVideo, AdCreative
from facebookads.api import FacebookAdsApi
from facebookads import FacebookSession
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.ad import Ad
from facebookads.adobjects.advideo import AdVideo
import os
import json
from datetime import datetime, timedelta, time
import pytz
import re
from utils.funcs import (remove_specified_key,
                              replace_key_name,
                              add_fields,
                              pickup_specified_key,
                              cast_to_dict,
                              str_to_int,
                              detect_device_type,
                              add_fields_case
                              )
from db.ads.ads import find_account_id, find_product_id, find_media_id
from report.ads.Manager.manager import AdAPItManager


class Reports(AdAPItManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._promotion_id = kwargs['promotion_id']
        # usually this is overwritten but fb has to add 'act_' before id
        self._media_account_id = 'act_' + kwargs['media_account_id']
        self._campaign_id = kwargs['media_campaign_id']
        self.all_date = None
        self.init_accounts = []
        self._campaigns = []
        self.inited_adsets = []
        self._level = 'adset'
        self._date_preset = ''
        self._fields = []
        self._time_range = {}
        self.session = ''

    def initialize(self,session):
        self.session = session

        # read config file
        this_dir = os.path.dirname(__file__)
        config_filename = os.path.join(this_dir, 'config.json')
        # path = os.path.join(this_dir, 'config.json')
        with open(config_filename) as config_file:
            config = json.load(config_file)

        # init account
        # proxies = {'http': '<HTTP_PROXY>', 'https': '<HTTPS_PROXY>'} # add proxies if needed
        api = FacebookAdsApi.init(access_token=config['access_token'])

        account = AdAccount(self._media_account_id)
        campaign = Campaign(self._campaign_id)
        adsets = AdSet(self._media_account_id)
        if self._type == 'campaign':
            account = Campaign(self._media_account_id)

        self.init_accounts.append(account)
        self._campaigns.append(campaign)
        self.inited_adsets.append(adsets)

        # init params
        f = adsinsights.AdsInsights.Field
        self._params = {
            'level': self._level[1],
            'date_preset': AdsInsights.DatePreset.yesterday,
            'time_range': {
                'since': self.start_time.strftime('%Y-%m-%d'),
                'until': self.end_time.strftime('%Y-%m-%d'),
            },
            'time_increment': self.granularity,
            'fields': [
                f.campaign_name,
                f.adset_name,
                f.spend,
                f.actions,
                f.impressions,
                f.app_store_clicks,
                f.campaign_id,
                f.adset_id,
            ],
            'today': datetime.now().strftime('%Y-%m-%d'),
        }

    def get_date_range(self):
        days = self._end_time - self._start_time
        list_of_date = [(self._start_time + timedelta(n)).strftime('%Y-%m-%d') for n in range(days.days)]
        return list_of_date, int(days.days)

    def update_params(self, level):
        if level not in ['ad', 'adset']:
            raise ValueError('you have to set "ad " or "adset" . Default is "adset" ')

        # switch level
        if level == 'ad':
            self._level = 'ad'
            self._params['fields'].append(adsinsights.AdsInsights.Field.ad_id)
            self._params['fields'].append(adsinsights.AdsInsights.Field.ad_name)

        if self._date_preset != []:
            self._params['date_preset'] = self._date_preset

        self._params['level'] = self._level

        if self._fields != []:
            self._params['fields'] = self._fields

        self._time_range = {
            'since': self._start_time.strftime('%Y-%m-%d'),
            'until': self._end_time.strftime('%Y-%m-%d')
        }
        self._params['time_range'] = self._time_range


    def _load_sync_data(self, level='adset'):
        self.validate_date_range()
        self.update_params(level)
        # self.all_date = (account.get_insights(params=self._params) for account in self.init_accounts)
        self.all_date = (campaing.get_insights(params=self._params) for campaing in self._campaigns)

    def _export_data(self):
        _data = []
        for data in self.all_date:
            for job in data:
                job.export_all_data()
                job.pop('date_stop')
                _data.append(job)

        # cast , add ,replace , remove kyes or columns
        __data = cast_to_dict(_data)
        d = replace_key_name(__data, 'date_start', 'date')
        d = replace_key_name(d, 'app_store_clicks', 'clicks')
        d = add_fields(d, 'promotion_id', self._promotion_id)

        # if a report type is ''account
        if self._type == 'account':
            print('ACCOUNT??')
            # d = add_fields_case(d, 'device','campaign_name',detect_device_type)

        _d = pickup_specified_key(d, 'actions', 'mobile_app_install', 'cvs')
        data = remove_specified_key(_d, 'actions')
        self._rows = str_to_int(data)

        ###
        # HAVE to imprelent promotion id divider
        ###

class CampaignReport(Reports):
    def export_campaign_report(self):
        self._load_sync_data()
        self._export_data()

    pass
