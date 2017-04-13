from utils.funcs import validate_login, get_addon_by_groups, reshape_orm_result, today, yesterday
from db.ads import ads
from flask_cors import CORS, cross_origin
from flask import redirect, request, render_template, url_for, jsonify, Blueprint
from report.ads.Dashboard.dashboard import Dashboard
from report.ads.Dashboard.get import Manager as DBManager
from report.ads.Dashboard.resister import Resister
from report.ads.Dashboard.updater import Updater
from report.ads.Manager.manager import Get

import json
from datetime import datetime, timedelta
from report.ads.Facebook.Reports import CampaignReport as FBCampaignReport
from report.ads.Manager.worker import fb_campagin_report_worker, im_campagin_report_worker, \
    tw_campagin_report_worker, nend_campagin_report_worker
from report.ads.Nend.report import CampaignReport as NendCampaignReport
from report.ads.Twitter.report import CampaignReport as TWCampaignReport
from report.ads.imobile.report import CampaignReport as IMCampaignReport
from report.ads.Manager.ads_db_manager import Manager

# bind db connection
session = ads.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('ads', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# run task manager
###########################
@app.route('/api/v1/run_tasks_manager', methods=['GET', 'POST'])
def run_tasks_manager():
    if request.method == 'GET':

        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time is None or end_time is None:
            start_time = yesterday().strftime('%Y-%m-%d')
            end_time = today().strftime('%Y-%m-%d')

        im, tw, fb, nend = Manager.queue_all_tasks()

        print(fb)
        for _fb in fb:
            fb_campagin_report_worker(FBCampaignReport, _fb, start_time, end_time)

        for _im in im:
            im_campagin_report_worker(IMCampaignReport, _im, start_time)

        for _nend in nend:
            nend_campagin_report_worker(NendCampaignReport, _nend, start_time)

        # for _tw in tw:
        #      tw_campagin_report_worker(TWCampaignReport, _tw)

        header, kpis = Dashboard.get_daily_report_by_promotion(start_time, end_time)
        data = {"header": header, "data": kpis}
        return jsonify(data=data)

    return jsonify(data='done!!')


###########################
# get
###########################
@app.route('/api/v1/get_promotion_list', methods=['GET', 'POST'])
def get_promotion_list():
    if request.method == 'GET':
        all_promotion = DBManager.get_promotion_list()
        return jsonify(data=all_promotion)



@app.route('/api/v1/init_resister_account', methods=['GET', 'POST'])
def init_resister_account():
    if request.method == 'GET':
        data = Get()
        accounts = data.get_accounts()
        products = data.get_all_products()
        medias = data.get_meidas()
        device = data.get_device()

        res = [
            accounts,
            products,
            medias,
            device,
        ]

        print('>>>>>>>>>>>>>.')
        print(accounts, medias, device, products, )

        return jsonify(data=res)


@app.route('/api/v1/get_account', methods=['GET', 'POST'])
def get_account():
    if request.method == 'GET':
        data = Get()
        _id = request.args.get('id')
        data = data.get_account(_id)
        return jsonify(data=data)


@app.route('/api/v1/get_products', methods=['GET', 'POST'])
def get_products():
    if request.method == 'GET':
        data = Get()
        account_id = request.args.get('account_id')
        product_name = request.args.get('product_name')
        products = data.get_products(account_id)
        # data = data.get_product(account_id,product_name)
        return jsonify(data=products)


@app.route('/api/v1/get_medias', methods=['GET', 'POST'])
def get_medias():
    if request.method == 'GET':
        data = Get()
        medias = data.get_meidas()
        return jsonify(data=medias)


@app.route('/api/v1/get_promotions', methods=['GET', 'POST'])
def get_promotions():
    if request.method == 'GET':
        data = Get()
        promotions = data.get_promotions()
        return jsonify(data=promotions)


###########################
# register
###########################
@app.route('/api/v1/resister_promotion', methods=['GET', 'POST'])
def resister_promotion():
    if request.method == 'POST':

        payload = request.get_json()

        print('>>>>>>>>>>>>>>>>')
        print('PAYLOAD')
        print(payload)

        resister = Resister()
        promotion_id = resister.resister_promotion(**payload)

        # resister relevant to table
        pid = {'id': promotion_id, }
        fee = {'id': promotion_id, 'fee': 1.2}

        resister.resister_ad_fee(**fee)
        resister.resister_monthly_budget(**pid)
        resister.resister_staff(**pid)
        resister.resister_istool(**pid)
        return jsonify(data=200)
    return jsonify('error')


@app.route('/api/v1/register_reporting_tasks', methods=['GET', 'POST'])
def register_reporting_tasks():
    if request.method == 'POST':
        print('>>>>>>>>>>>>>>>>>>>>>>>')
        print('REGISTER_REPORTING_TASKS')
        payload = request.get_json()
        print(payload)
        resister = Resister()
        # manager = DBManager()
        media_campaign_id = payload.get('media_campaign_id', False)

        if media_campaign_id is False:

            ad_report = {
                'promotion_id': payload['id'],
                'media_account_id': payload['media_account_id'], }
        else:
            ad_report = {
                'promotion_id': payload['id'],
                'media_account_id': payload['media_account_id'],
                'media_campaign_id': payload['media_campaign_id'],
            }

        resister.resister_ad_report_manager(**ad_report)

        return jsonify(data=200)
    return jsonify('error')


@app.route('/api/v1/resister_account', methods=['GET', 'POST'])
def resister_account():
    if request.method == 'POST':
        register = Resister()
        data = Get()
        res = request.get_json()
        act_id = register.resister_ad_account(res['account_name'])
        act = data.get_account(act_id)
        return jsonify(data=act)

    print('error')
    return jsonify(data='error')


@app.route('/api/v1/resister_product', methods=['GET', 'POST'])
def resister_product():
    if request.method == 'POST':
        register = Resister()
        data = Get()
        res = request.get_json()
        print('RESISTER_PRODUCT')
        p_id = register.resister_products(res['account_id'], res['product_name'])
        product = data.get_product(p_id)

        return jsonify(data=product)

    print('error')
    return jsonify(data='error')


###########################
# update
###########################
@app.route('/api/v1/update_ad_fee', methods=['GET', 'POST'])
def update_ad_fee():
    if request.method == 'POST':
        print('>>>>>>>>>>>>>>>>>>>>>>>')
        print('RESISTER_PROMOTION')
        payload = request.get_json()

        print(payload)

        Updater.update_ad_fee(**payload)
        promotion_list = DBManager.get_promotion_list()

        return jsonify(data=promotion_list)
    return jsonify('error')

@app.route('/api/v1/update_m_budget', methods=['GET', 'POST'])
def update_m_budget():
    if request.method == 'POST':
        payload = request.get_json()
        Updater.update_ad_budget(**payload)
        promotion_list = DBManager.get_promotion_list()
        return jsonify(data=promotion_list)
    return jsonify('error')


@app.route('/api/v1/update_staff', methods=['GET', 'POST'])
def update_staff():
    if request.method == 'POST':
        payload = request.get_json()
        Updater.update_staff(**payload)
        promotion_list = DBManager.get_promotion_list()
        return jsonify(data=promotion_list)
    return jsonify('error')


@app.route('/api/v1/update_program_name', methods=['GET', 'POST'])
def update_program_name():
    if request.method == 'POST':
        payload = request.get_json()
        Updater.update_program_name(**payload)
        promotion_list = DBManager.get_promotion_list()
        return jsonify(data=promotion_list)
    return jsonify('error')


@app.route('/api/v1/update_program_id', methods=['GET', 'POST'])
def update_program_id():
    if request.method == 'POST':
        payload = request.get_json()
        Updater.update_program_id(**payload)
        promotion_list = DBManager.get_promotion_list()
        return jsonify(data=promotion_list)
    return jsonify('error')


@app.route('/api/v1/update_promotion_list', methods=['GET', 'POST'])
def update_promotion_list():
    if request.method == 'POST':
        print('>>>>>>>>>>>>>>>>>>>>>>>')
        print('UPDATE_PROMOTION_LIST')
        payload = request.get_json()
        promotion = DBManager.get_promotion(payload['id'])

        _promotion = {
            'account_name': payload['account_name'],
            'budget': payload['budget'],
            'device_name': payload['device_name'],
            'fee':payload['fee'],
            'id': payload['id'],
            'media_name': payload['media_name'],
            'product_name':payload['product_name'],
            'program_id': payload['program_id'],
            'program_name': payload['program_name'],
            'staff_name': payload['staff_name'],
        }

        # order is important to compare existed and updated data
        _promotion = [
            payload['id'],
            payload['account_name'],
            payload['product_name'],
            payload['media_name'],
            payload['device_name'],
            payload['fee'],
            payload['budget'],
            payload['program_name'],
            payload['program_id'],
            payload['staff_name'],
        ]

        for i, (p, _p) in enumerate(zip(promotion,_promotion)):
            print(p[i],_p)
            if p[i] != _p:
                print(_p)

        return jsonify(data=200)
    return jsonify('error')


###########################
# delete
###########################





###########################
# get report
###########################
@app.route('/api/v1/get_daily_report_by_promotion', methods=['GET', 'POST'])
def get_daily_report_by_promotion():
    if request.method == 'GET':
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time is None or end_time is None:
            start_time = yesterday().strftime('%Y-%m-%d')
            end_time = today().strftime('%Y-%m-%d')

        header, kpis = Dashboard.get_daily_report_by_promotion(start_time, end_time)
        data = {"header": header, "data": kpis}
        return jsonify(data=data)


@app.route('/api/v1/get_report_by_media', methods=['GET', 'POST'])
def get_report_by_media():
    if request.method == 'GET':
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time is None or end_time is None:
            start_time = yesterday().strftime('%Y-%m-%d')
            end_time = today().strftime('%Y-%m-%d')

        header, kpis = Dashboard.get_report_by_media(start_time, end_time)
        data = {"header": header, "data": kpis}
        return jsonify(data=data)


@app.route('/api/v1/get_report_by_product', methods=['GET', 'POST'])
def get_report_by_product():
    if request.method == 'GET':
        # try:
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time is None or end_time is None:
            start_time = yesterday().strftime('%Y-%m-%d')
            end_time = today().strftime('%Y-%m-%d')

        header, kpis = Dashboard.get_report_by_product(start_time, end_time)
        data = {"header": header, "data": kpis}
        return jsonify(data=data)

