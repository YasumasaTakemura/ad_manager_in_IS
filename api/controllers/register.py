#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login,reshape_orm_result
from flask_cors import CORS, cross_origin
from flask import redirect, request, render_template, url_for, jsonify
from flask import Blueprint
from flask.ext.login import LoginManager, login_required, login_user, logout_user, user_logged_out, \
    user_logged_in
from sqlalchemy import delete
from sqlalchemy_fulltext import FullText, FullTextSearch
import sqlalchemy_fulltext.modes as FullTextMode
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from sqlalchemy import asc, desc
import requests
from twitter_ads.http import Request as tw_request
from twitter_ads.client import Client
from db.admin import admin
import json
from datetime import datetime
import boto3

import jwt
from datetime import *

# bind db connection
session = admin.session



# crate blueprint
app = Blueprint('register', __name__)

# crate corn object
CORS(app, resources={r"/*": {"origins": "*"}})


# nomal function
def support_datetime_default(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()
    raise TypeError(repr(dt) + " is not JSON serializable")




@app.route("/q", methods=['GET', 'POST'])
def q():
    return jsonify(data=[{'data': 'json1!'},
                         {'data': 'json2!'},
                         {'data': 'json3!'}])


# first endopint
@app.route("/top", methods=['GET', 'POST'])
@login_required
def top():
    # init dataset
    dataset = None
    finished_list = None

    columns = admin.ToDoList.__table__.columns.keys()[3:11]

    try:
        datasorce = request.args.get('dataset')
        dataset = json.loads(datasorce)
        print(dataset)
        return render_template('top.html', dataset=dataset, columns=columns, finished_list=finished_list)

    except:
        return render_template('top.html', dataset=dataset, columns=columns, finished_list=finished_list)


# first endopint
@app.route("/top_pre", methods=['GET', 'POST'])
@login_required
def top_pre():
    return render_template('top_pre.html')


@app.route("/register")
def register():
    todolist_columns = admin.ToDoList.__table__.columns.keys()[2:11]
    return render_template('account_register.html', todolist_columns=todolist_columns)


##########################
# Form 
##########################

@app.route("/register_form", methods=['GET', 'POST'])
def register_form():
    if request.method == "POST":

        # validate header
        # split() is to eliminate options like,  'application/json';charset=UTF-8 ...
        if request.headers['Content-Type'].split(';', 1)[0] != 'application/json':
            print(request.headers['Content-Type'])
            return jsonify(res='error'), 400

        # get table columns and assign variables
        table = admin.FormTemplate.__table__.columns.keys()[1:]
        print(table)
        template = {}

        forms = request.get_json()

        if forms == '' or forms == None:
            return jsonify(res='<alert("empty");>'), 200

        # validate empty
        if not forms['title']:
            print('empty')
            return jsonify(res='<alert("empty");>'), 200

        for form in forms['form']:
            for k, v in form.items():
                if not v:
                    pass
                    # return jsonify(res='<alert("empty");>'), 200
        '''
                            temp.update({form['name']: form['value']})
                            list.append(temp)
                            temp = {}
                            pass

                    temp.update({form['name']: form['value']})

                template['template'] = list
                form_object.update(template)
        '''

        # create sqlalchemy obj
        for i in table:
            if i == 'manager_id':
                user_id = admin.find_user_id(validate_login(db,session))
                template.update({i: user_id})

            elif i == 'form_title':
                template.update({'form_title': forms['title']})


            else:
                template.update({'template': forms['form']})

        print(template)

        try:
            session.rollback()
            session.add(admin.FormTemplate(**template))
            session.commit()
            session.close()
            return jsonify(res='success')
        except IntegrityError:
            return jsonify(res='error')


@app.route("/get_form_template", methods=['GET', 'POST'])
def get_form_template():
    session.rollback()
    data = session.query(admin.FormTemplate).filter(
        admin.FormTemplate.manager_id == admin.find_user_id(validate_login(db,session))).all()
    shaped_data = reshape_orm_result(data)

    print('------------')
    print(shaped_data)
    return jsonify(data=shaped_data)


@app.route("/form_creation", methods=['GET', 'POST'])
@login_required
def form_creation():
    return render_template('form_creation.html')


'''
@app.route("/register_form_template", methods=['GET', 'POST'])
@login_required
def regist_form_template():
    if request.method == "POST":

        # check header
        if request.headers['Content-Type'] != 'application/json':
            print(request.headers['Content-Type'])
            return jsonify(res='error'), 400

        # get table columns and assign variables
        table = admin.FormTemplate.__table__.columns.keys()[1:]
        temp = {}
        template = {}
        form_object = {}
        list = []

        data = request.get_json().get('data')
        print(data)

        if data == '' or data == None:
            return jsonify(res='<alert("empty");>'), 400

        # parse json data from Form object
        for d in data:
            if d['name'] == 'form_title':
                print(d['name'])
                continue

            if d['name'] == 'comment':
                temp.update({d['name']: d['value']})
                list.append(temp)
                temp = {}
                pass

            temp.update({d['name']: d['value']})

        template['template'] = list
        form_object.update(template)

        # create sqlalchemy obj
        for i in table:
            if i == 'manager_id':
                user_id = admin.find_user_id(current_user.username)
                form_object.update({i: user_id})

            elif i == 'form_title':
                form_object.update({data[0]['name']: data[0]['value']})

        print(form_object)

        try:
            session.rollback()
            session.add(admin.FormTemplate(**form_object))
            session.commit()
            session.close()
            return redirect(url_for('register.form_creation'))
        except IntegrityError:
            return jsonify(res='error')


'''


@app.route("/delete_form_template", methods=['GET', 'POST'])
@login_required
def delete_form_template():
    if request.method == "POST":
        form_id = request.get_json().get('id')
        print(form_id)
        try:
            session.query(admin.FormTemplate).filter(admin.FormTemplate.form_id == form_id).delete()
            session.commit()
            session.close()
            return jsonify(res='success')

        except SQLAlchemyError:
            print('rolled back')
            session.rollback()
            return jsonify(res='error')


## Todolist ##
@app.route('/create_todolist', methods=['GET', 'POST'])
def create_todolist():
    if request.method == 'POST':
        user_id = admin.find_user_id(current_user.username)

        ToDoList_col = admin.ToDoList.__table__.columns.keys()[:-3]

        account = request.form.get('account')

        # check exist the account
        account_id = admin.account_register(current_user.username, account)

        print(account_id)

        temp = {}
        for i in ToDoList_col:
            if i == 'start' and isinstance(request.form.get(i), str):
                temp.update({i: datetime.strptime(request.form.get(i), '%Y-%m-%dT%H:%M')})


            elif i == 'end' or i == 'due_day' and isinstance(request.form.get(i), str):
                if i != str:
                    temp.update({i: None})

                else:
                    temp.update({i: datetime.strptime(request.form.get(i), '%Y-%m-%dT%H:%M')})


            elif i == 'account_id':
                temp.update({i: account_id})

            elif i == 'user_id':
                temp.update({i: user_id})

            elif i == 'todo_id':
                pass

            else:
                print('------------')
                temp.update({i: request.form.get(i)})

        # session.rollback()
        session.add(admin.ToDoList(**temp))
        session.commit()
        return redirect(url_for('register.top'))


@app.route("/delete_mytodolist", methods=['GET', 'POST'])
@login_required
def delete_mytodolist():
    if request.method == "POST":
        todo_id = request.get_json().get('id')
        print(todo_id)
        try:
            session.query(admin.ToDoList).filter(admin.ToDoList.todo_id == todo_id).delete()
            session.commit()
            session.close()
            return jsonify(res='success')

        except SQLAlchemyError:
            print('rolled back')
            session.rollback()
            return jsonify(res='error')


@app.route('/get_all_mytodolist', methods=['GET', 'POST'])
def get_all_mytodolist():
    if request.method == 'GET':
        user_id = admin.find_user_id(validate_login(db,session))
        data = admin.session.query(admin.ToDoList).filter(admin.ToDoList.user_id == user_id,
                                                    admin.ToDoList.finished == False).all()
        shaped_data = reshape_orm_result(data)
        print(type(data))
        print(len(data))
        return jsonify(data=shaped_data)


@app.route('/get_finished_list', methods=['GET', 'POST'])
def get_finished_list():
    if request.method == 'GET':
        user_id = admin.find_user_id(current_user.username)
        data = admin.session.query(admin.ToDoList).filter(admin.ToDoList.user_id == user_id,
                                                    admin.ToDoList.finished == True).all()
        shaped_data = reshape_orm_result(data)

        # print(shaped_dataset)
        print('new')
        print(type(shaped_data))
        print(len(shaped_data))

        return jsonify(data=shaped_data)


@app.route('/get_incoming_request', methods=['GET', 'POST'])
def get_incoming_request():
    if request.method == 'GET':
        user_id = admin.find_user_id(current_user.username)
        finished_list = admin.session.query(admin.ToDoList).filter(admin.ToDoList.user_id == user_id,
                                                             admin.ToDoList.finished == True).all()

        shaped_datasource = reshape_orm_result(finished_list)

        print(shaped_datasource)

        return jsonify(data=shaped_datasource)


@app.route('/get_inputtype', methods=['GET', 'POST'])
def get_inputtype():
    if request.method == 'GET':
        return


@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
    s3_client = boto3.client('s3')
    # Upload the file to S3
    s3_client.upload_file('test.txt', 'bucket-name', 'test-remote.txt')


@app.route('/get_files', methods=['GET', 'POST'])
def get_files():
    s3 = boto3.resource('s3')
    bucket = 'admanager-log'
    bucket = s3.Bucket(bucket)
    print(bucket.name)
    lis = []
    [lis.append(obj_summary.key) for obj_summary in bucket.objects.all()]
    print(lis)

    '''
    presigned_post = s3.generate_presigned_post(
        Bucket=bucket,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    print(presigned_post)


    s3 = boto3.client('s3')
    file_name = 'demo5/tw/Screen Shot 2016-08-02 at 13.34.28.png'
    presigned_post = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': file_name},
        ExpiresIn=3600,
        HttpMethod='GET')

    # signed_url ={'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)}
    signed_url = {'url': 'https://s3-ap-northeast-1.amazonaws.com/%s/%s/%s' % (bucket, 'clients', file_name)}
    print(signed_url)

    return json.dumps({
        'data': presigned_post,
        'url': signed_url
    })
    '''

    return '<img src="https://s3-ap-northeast-1.amazonaws.com/admanager-log/favicon.png">'


'''
###########################
# Task Lists
###########################

@app.route('/get_tasks', methods=['GET', 'POST'])
def get_tasks():
    if request.method == 'GET':
        print('get tasks')
        user_id = admin.find_user_id(validate_login(db,session))
        data = admin.session.query(admin.TaskList).filter(admin.TaskList.userID == user_id,
                                                    admin.TaskList.completed == False).all()
        data = reshape_orm_result(data)
        print(data)
        print(len(data))
        return jsonify(data=data)

'''


@app.route('/', methods=['GET', 'POST'])
def api():
    ad_layer = {
        'campaign': 'campaign_name',
        'adset': 'adset_name',
        'ad': 'ad_name',
    }

    datasource = []

    if request.method == 'POST':
        level = request.form.get('layer')

        since = tools.date_to_today(request.form.get('since'))
        until = tools.date_to_today(request.form.get('until'))

        # level = ad_layer.get(level)
        # print('l:{},s:{} ,u:{}'.format(level, since, until))

        ##Facebook##
        # pd.options.display.float_format = '{:,.0f}'.format


        ##for an initiation
        my_access_token = 'EAAJTsDvqlrwBALaTJ7GE5zuj3wdi3AXRF56VRS4edxI6O5h83DMJBefeboXC78hwffGU4vOE7pYyn3wPVNdkL3CizSc129XwzHlfRCnNmY3ptOEO7zACoSnjQoYzZBJodZC2kHi3ZCVh7OWVPGSVI4ZCGcVZBltBrPAhEtvptGwZDZD'
        fields = '{},spend,actions,impressions,app_store_clicks'.format(ad_layer.get(level))
        data_preset = 'yesterday'
        time_increment = 0

        # endpoint
        act_id = '1145204765515702'
        fb_endpoint = 'https://graph.facebook.com/v2.7/act_{}/insights'.format(act_id)
        parameter = '?access_token={}&fields={}&level={}&date_preset={}&time_range[since]={}&time_range[until]={}'.format(
            my_access_token, fields, level, data_preset, since, until)

        fb_request = fb_endpoint + parameter

        rq = requests.get(fb_request).json()

        # retrieve fb ads data
        level = ad_layer.get(level)
        fb_datasource = tools.fb_api(rq['data'], level)

        ##Twitter##
        CONSUMER_KEY = 'm6irZiH74Il69q1fr4QziiDfK'
        CONSUMER_SECRET = 'rSTzU1Ft4dFoQo36KtwCSnAETHqswbrQSoR3N9pUOEL9RWfiIX'
        ACCESS_TOKEN = '2936980603-FfmXtKAdczIFyt0pawDJ8PxIDW0ZNyfYbH9XKAg'
        ACCESS_TOKEN_SECRET = 'g6gHfa1Mr1njFpFmYa4SOnV2DDykRqst122jVbkIREOfv'

        ACCOUNT_ID = '18ce54crrcq'  # ブレクロ
        ACCOUNT_ID = '18ce53y8414'  # ブレクロ

        acounts = ['18ce54crrcq', '18ce53y8414']

        # initialize the client
        client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        account = client.accounts(ACCOUNT_ID)

        Acounts = [client.accounts(act) for act in acounts]

        # REQUEST PARAMETER

        param = {
            'START_TIME': since,
            'END_TIME': until,
            'METRIC': 'ENGAGEMENT,BILLING,WEB_CONVERSION,MEDIA',
            'endpoint': '/1/stats/accounts/{}'.format(account.id)
        }

        param = {
            'START_TIME': since,
            'END_TIME': until,
            'METRIC': 'MOBILE_CONVERSION,ENGAGEMENT,BILLING',
            'endpoint': '/1/stats/accounts/{}'.format(account.id)
        }

        param = {
            'START_TIME': since,
            'END_TIME': until,
            'METRIC': 'MOBILE_CONVERSION,ENGAGEMENT,BILLING',
            'endpoint': '/1/stats/jobs/accounts/{}'.format(account.id)
        }
        '''
        tw_datasource = tools.tw_api_sync(client, Acounts, param)
        if tw_datasource[0] == 'INVALID_TIME_WINDOW':
            return render_template('data_viewer.html', json=[], ad_layer=ad_layer)
        '''
        datasource.extend(fb_datasource)
        # datasource.extend(tw_datasource)

        print(datasource)
        print(type(datasource))

    return render_template('data_viewer.html', json=datasource, ad_layer=ad_layer)
