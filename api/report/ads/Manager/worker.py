import queue
import time as timer
from threading import Thread
from utils.funcs import today, yesterday
from twitter_ads.campaign import LineItem
from db.ads import ads


def threaded(f, daemon=False):
    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = queue.Queue()

        t = Thread(target=wrapped_f, args=(q,) + args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap


#
#
# fb,tw,adw,im,nd,yh = Manager.all_tasks()

# print(self.read_files('accounts.json'))
# self.account_ids = [act[id] for act in  self.read_files('accounts.json')['accounts'][0]]
# print(self.account_ids)

# for initiation
_start_time = yesterday().strftime('%Y-%m-%d')
_end_time = today().strftime('%Y-%m-%d')


adjust_params = {

    'time_range': {
        'start_time': '2017-03-01',
        'end_time': '2017-03-14',
    },

    'ip_address': '',
    'id': {
        'username': 'email',
        'password': 'password',
    },
    'login': {
        'url': 'https://next.adjust.com/#/login',
        'username': '',
        'password': '',
        'submit': '',
        'submit_text_link': 'Login',
    }

}


def fb_campagin_report_worker(cls, act, start_time=_start_time, end_time=_end_time):
    session = ads.session
    report = cls(**act)
    report.initialize(session)
    report.start_time = start_time
    report.end_time = end_time
    report.export_campaign_report()
    report.upsert_campaign_report()
    d = report.dataset

    # if not blocking with this timer
    # db exhaust error which is blocking or closed
    timer.sleep(3)


def tw_campagin_report_worker(cls,act, start_time=_start_time, end_time=_end_time):
    session = ads.session
    report = cls(**act)
    report.initialize(session)
    # report.preview_tweet()
    report.start_time = start_time
    report.end_time = end_time
    report.export_campaign_report()
    report.upsert_campaign_report()
    d = report.dataset
    # print(d)
    # print()


def im_campagin_report_worker(cls, act, start_time=_start_time, end_time=_end_time):
    report = cls(**act)
    report.initialize()
    report.start_time = start_time
    report.export_campaign_report()
    report.upsert_campaign_report()
    d = report.dataset


def nend_campagin_report_worker(cls, act, start_time=_start_time, end_time=_end_time):
    report = cls(**act)
    report.initialize()
    report.start_time = start_time
    report.export_campaign_report()
    report.upsert_campaign_report()
    d = report.dataset


def adjust_report(cls):
    ins = cls()
    ins.initialize()
    ins.read_files('accounts.json')
    ins.params = adjust_params
    # ins.export_data()
    ins.parse_table()


def tw_creative_report_worker(cls, days):
    print('>>>>>>>>>')
    instance = cls()
    instance.initialize()
    instance.preview_tweet()

    # instance.range=days

    # instance.end_time=datetime.strptime('2017-02-01', '%Y-%m-%d')
    instance.end_time = '2017-03-14'
    instance.start_time = '2017-01-01'

    instance.load_async_data(LineItem)
    instance.export_data()
    list_of_date, _ = instance.get_date_range()
    d = instance.all_data
    print('>>>>>>>>>>>> RESULT')
