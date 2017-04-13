import time as timer
from twitter_ads.client import Client
from twitter_ads.campaign import LineItem
from twitter_ads.campaign import Tweet
from twitter_ads.creative import PromotedTweet, WebsiteCard, ImageAppDownloadCard, VideoAppDownloadCard
from twitter_ads.enum import METRIC_GROUP, GRANULARITY
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, time
import os
import pickle
from utils.funcs import date_to_int, detect_device_type, add_fields
from report.ads.Manager.manager import AdAPItManager


# this class is super class for Campaign and Creative report
class Report(AdAPItManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account = None  # for tw client object
        self.account_info = None
        self._type_account = kwargs['type_account']
        self.all_campaigns = None
        self.all_line_items = None
        self.all_tweets = None
        self.cid_lid = None
        self.twid_lid = None

        self._params = {
            'promotion_id': '',
            'media_account_id': '',
        }
        self.metric_groups = [
            METRIC_GROUP.MOBILE_CONVERSION,
            METRIC_GROUP.WEB_CONVERSION,
            METRIC_GROUP.ENGAGEMENT,
            METRIC_GROUP.BILLING,
            METRIC_GROUP.MEDIA,
        ]
        self._list_of_date = []

    # have to call this method after instance was newed
    def initialize(self, session):

        # init account
        CONSUMER_KEY = self.read_files('keys.json')['CONSUMER_KEY']
        CONSUMER_SECRET = self.read_files('keys.json')['CONSUMER_SECRET']
        ACCESS_TOKEN = self.read_files('keys.json')['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = self.read_files('keys.json')['ACCESS_TOKEN_SECRET']

        client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        print('ACCOUNT')
        self.account = client.accounts(self._media_account_id)

        self._params = {
            'start_time': self._start_time,
            'end_time': self._end_time,
            'granularity': self._granularity,
            'today': datetime.now().strftime('%Y-%m-%d'),
            'segmentation_type':'PLATFORMS'
        }

        if self.all_campaigns is None:
            self.all_campaigns = self.account.campaigns()

        if self.all_line_items is None:
            self.all_line_items = list(self.account.line_items(None, count=20))
            print('LEN')
            print(len(self.all_line_items))

        self.account_info = self._join_cid_and_lid()

    # only for joining data in this instance
    def _join_cid_and_lid(self):
        joined_data = []
        for campaign in self.all_campaigns:
            print('CAMPAIGN_NAME')
            print(campaign.name)
            print(campaign.id)
            for line_item in self.all_line_items:
                if line_item.campaign_id == campaign.id:
                    joined_data.append({'campaign_id': line_item.campaign_id, 'adset_id': line_item.id,
                                        'campaign_name': campaign.name})

        return joined_data

    def __update_param(self):
        # if params is None: return {}
        self._params['start_time'] = self._start_time
        self._params['end_time'] = self._end_time
        self._params['granularity'] = GRANULARITY.DAY


    def __chunk(self, items, n):
        chunk = []
        for i, item in enumerate(items):
            chunk.append(item)
        return (chunk[i:n + i] for i in range(0, len(chunk), n))


    def __get_date_range(self):
        days = self._end_time - self._start_time
        list_of_date = [(self._start_time + timedelta(n)).strftime('%Y-%m-%d') for n in range(days.days)]
        return list_of_date, int(days.days)


    # join each line items
    def __join_all(self, data):
        temp = []
        for act in self.account_info:
            for item in data:
                if item['adset_id'] == act['adset_id']:
                    item.update({'campaign_name': act['campaign_name'], 'campaign_id': act['campaign_id']})
                    temp.append(item)
        return temp


    def __load_sync_data(self, Cls):
        resources = []

        # load line items
        if Cls == LineItem:
            resources = self.__chunk(self.all_line_items, 20)

        # load creatives
        elif Cls == PromotedTweet:
            resources = self.all_tweets

        for i, items in enumerate(resources):
            items[i].stats(self.metric_groups)
            ids = [i.id for i in items]

            res = Cls.all_stats(self.account, ids, self.metric_groups)
            _spend = res[0]['id_data'][0]['metrics']['billed_charge_local_micro']
            if _spend is not None:
                self._rows.append(_spend)


    # to get data from ads api by async
    def _load_async_data(self, Cls):

        # line_items = self.chunk(self.all_line_items, 20)
        resources = []
        if Cls == LineItem:
            resources = self.__chunk(self.all_line_items, 20)

        if Cls == Tweet:
            resources = self.all_tweets

        for i, items in enumerate(resources):

            items[i].stats(self.metric_groups)
            ids = [i.id for i in items]

            self.validate_date_range()
            self.__update_param()

            # fetching async stats on the instance
            queued_job = Cls.queue_async_stats_job(self.account, ids, self.metric_groups, **self._params)

            # get the job_id:
            job_id = queued_job['id']

            # for looping to job requests
            # we have to wait to get jobs done
            loading_status = True

            timer.sleep(15)

            # let the job complete
            while loading_status:

                # interval for getting request
                timer.sleep(15)
                async_stats_job_result = Cls.async_stats_job_result(self.account, job_id)
                _async_data = Cls.async_stats_job_data(self.account, async_stats_job_result['url'])

                if _async_data:
                    self._rows = _async_data['data']
                    print('>>>>>>>>>>>>>>>>>>.')
                    print(self._rows)
                    loading_status = False


    def set_pkl(self, data,path, filename):
        file = filename + '.pkl'
        file_path = os.path.join(path, file)
        pickle.dump(data, open(file_path, "wb"))


    def get_pkl(self, path, filename):
        file = filename + '.pkl'
        file_path = os.path.join(path, file)
        pkl = pickle.load(open(file_path, "rb"))
        print(pkl)


    # shape dataset
    def _export_data(self):
        # get list of datetime and int:days
        list_of_date, days = self.__get_date_range()

        _data = []
        for i in range(days):

            for j, row in enumerate(self._rows):


                if len(row['id_data']) == 0:
                    print(row)
                    continue

                promotion_id = ''
                os = row['id_data'][0]['segment']['segment_name'].split(' ')[0].lower()


                # match promotion_id with segment name (platform/device)
                for _type in self._type_account:
                    if os == _type['device']:
                        promotion_id = _type['promotion_id']


                temp = {
                    'date': list_of_date[i],
                    'adset_id': row['id'],
                    'promotion_id': promotion_id,
                }


                # add items
                for k, v in row['id_data'][0]['metrics'].items():
                    try:

                        if k == 'billed_charge_local_micro' and v:
                            temp.update({'spend': int(v[i] / 1000000)})

                        elif k == 'impressions' and v:
                            temp.update({'impressions': v[i]})

                        elif k == 'app_clicks' and v:
                            temp.update({'clicks': v[i]})

                        elif k == 'mobile_conversion_installs' and v['post_engagement'][i]:
                            temp.update({'cvs': v['post_engagement'][i]})

                    except Exception as e:
                        print(e)

                # pass if promotion_id is empty
                if promotion_id != '':

                    is_spend = temp.get('spend', False)
                    is_imp = temp.get('impressions', False)

                    if is_imp or is_spend:
                        _data.append(temp)

        self._rows = self.__join_all(_data)

    def preview_tweet(self):
        preview = Tweet.preview(self.account, id=834737275204362240)
        # preview = Tweet.preview(self.account, id=814012789953994752)
        print(preview)


class CampaignReport(Report):
    def export_campaign_report(self):
        self._load_async_data(LineItem)
        # self.get_pkl(os.getcwd(),'tw_test')
        self._export_data()


class FollowerReport(Report):
    def export_campaign_report(self):
        self._load_async_data(LineItem)
        'followers'
        # self.get_pkl(os.getcwd(),'tw_test')
        self._export_data()


class CreativeReport(Report):
    def export_creative_report(self):
        self._load_async_data(PromotedTweet)
        self._export_data()

    # only for to join data in this instance
    def _join_cid_lid_twid(self):
        joined_data = []
        for campaign in self.all_campaigns:
            for line_item in self.all_line_items:
                for tw in self.all_tweets:
                    if campaign['cid'] == line_item['cid'] and line_item['cid'] == tw['lid']:
                        d = {
                            'tweet_id': tw['tweet_id'],
                            'lid': line_item['lid'],
                            'id': tw['id'],
                            'cid': campaign['cid'],
                            'name': campaign['name'],
                        }
                        joined_data.append(d)
        return joined_data

    # to get data as prop
    @property
    def datasets(self):
        return self._rows

    # get ImageAppDownloadCard properties
    @property
    def app_images(self):
        all_app_cards = ImageAppDownloadCard.all(self.account)  # all() means load all of items
        all_app_image_fields = [{
                                    'id': card.id,
                                    'name': card.name,
                                    'url': card.wide_app_image,
                                    'thumbnail': card.preview_url,
                                    'wide_app_image_media_id': card.wide_app_image_media_id,
                                    'created_at': card.created_at,
                                    'updated_at': card.updated_at,

                                } for card in all_app_cards]
        return all_app_image_fields

    # get VideoAppDownloadCard properties
    @property
    def app_videos(self):
        all_app_video = VideoAppDownloadCard.all(self.account)
        all_video_fields = [{
                                'name': card.name,
                                'url': card.video_url,
                                'thumbnail': card.video_poster_url,
                                'id': card.id,
                                'created_at': card.created_at,
                                'updated_at': card.updated_at,

                            } for card in all_app_video]
        return all_video_fields

    # get promoted_tweet properties
    @property
    def promoted_tweet(self):
        all_promoted_tweet = PromotedTweet.all(self.account)
        all_promoted_tweet_fields = [{
                                         'id': card.id,
                                         'line_item_id': card.line_item_id,
                                         'tweet_id': card.tweet_id,
                                         'paused': card.paused,
                                         'created_at': card.created_at,
                                         'updated_at': card.updated_at,

                                     } for card in all_promoted_tweet]
        return all_promoted_tweet_fields

    # get ImageAppDownloadCard properties
    @property
    def website_card(self):
        all_website_card = PromotedTweet.all(self.account)
        all_website_card_fields = [{
                                       'id': card.id,
                                       'name': card.name,
                                       'preview_url': card.preview_url,
                                       'website_title': card.website_title,
                                       'website_url': card.website_url,
                                       'created_at': card.created_at,
                                       'updated_at': card.updated_at,

                                   } for card in all_website_card]
        return all_website_card_fields

    # get preview html
    def preview_tweet(self):
        preview = Tweet.preview(self.account, id=836468142947758081)
        print(preview)

    def __parse_preview_tweet_html(self):
        pass

    def parse_xml(self, xml_data):
        root = ET.fromstring(xml_data)
        print(xml_data)
        for child in root:
            print(child.MediaFile)
            return child.MediaFile
