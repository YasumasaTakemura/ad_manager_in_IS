#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result, parseSAtoJson, \
    join_table_with_additional_key
from db.admin import admin
from flask_cors import CORS, cross_origin
from flask import redirect, request, render_template, url_for, jsonify
from flask import Blueprint
from sqlalchemy import delete, asc, desc
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
import json
from datetime import datetime
import jwt
from datetime import *

# bind db connection
session = admin.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('groupManager', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# functions
###########################


def join_table(objects, key):
    _data = []
    for _object in objects:  # get rows
        __data = {}
        for obj in _object:  # get each key and value
            print(_object.group.manager_id)
            __data.update({key: _object.group.group_title})
            __data.update({obj[0]: obj[1]})
        _data.append(__data)
    return _data


###########################
# Group Managing
###########################


# test for grouping
@app.route('/get_groups', methods=['GET', 'POST'])
def get_groups():
    user_id = db.find_user_id(validate_login(db, session))
    groups = session.query(db.Group).filter(db.Group.manager_id == user_id).all()
    groups = parseSAtoJson(groups)
    print(groups)
    return jsonify(data=groups)


@app.route('/be_a_member', methods=['GET', 'POST'])
def be_a_member():
    print(request.get_json())
    username = validate_login(db, session)
    user_id = db.find_user_id(username)

    relation = session.query(db.GroupManager).join(db.GroupManager.group).filter(db.Group.manager_id == user_id,
                                                                                 db.GroupManager.status == 'inviting').first()

    # data = join_table(relation, request.get_json()['answer'])
    # print(data)
    try:
        if request.get_json()['answer'] == 'approve' and relation.status == 'inviting':
            relation.status = 'member'
            session.commit()
            return jsonify(data='became a member')
        elif request.get_json()['answer'] == 'approve' and relation.status == 'member':
            return jsonify(data='already a member')
        else:
            relation.status = 'declined'
            session.commit()
            return jsonify(data='declined')
    except Exception as e:
        print(e)
        return jsonify(data='no data')


# test for grouping
@app.route('/invite_as_member', methods=['GET', 'POST'])
def invite_as_member():
    member_id = request.get_json()['user']['user_id']
    group_id = request.get_json()['group']['group_id']
    current_user = validate_login(db, session)
    # user_id = db.find_user_id(current_user)

    print(member_id, group_id)

    try:
        relation = session.query(db.GroupManager).filter(db.GroupManager.member_id == member_id).first()
        print(relation.status)

        if relation.status == 'inviting':
            relation.status = 'member'
            session.commit()
            return jsonify(data='already invited')

        elif relation.status == 'member':
            return jsonify(data='already member')

    except:
        print('invite as new member')
        group = {
            'group_id': group_id,
            'member_id': member_id,
        }
        group = db.GroupManager(**group)

        session.add(group)
        session.commit()
        return jsonify(data='invited!')


# test for grouping
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    data = request.get_json()
    data = {'group_title': data['group']['group_title'],
            'manager_id': data['group']['manager_id'],
            'member_id': data['user']['user_id'],
            }

    member = db.GroupManager(**data)
    session.add(member)
    session.commit()
    return jsonify(data='member added')


# test for gruping
@app.route('/register_group', methods=['GET', 'POST'])
def register_group():
    try:
        username = validate_login(db, session)
        user_id = db.find_user_id(username)

        data = request.get_json()
        print(data)

        group = {
            'group_title': data['group_title'],
            'manager_id': user_id,
        }

        g = db.Group(**group)

        session.add(g)
        session.commit()

        return jsonify(data='register a group is done!!!')


    except IntegrityError as e:
        print(e)
        print('error')
        return jsonify(data='register a group is error!!!')


@app.route('/get_members_in_group', methods=['GET', 'POST'])
def get_members_in_group():
    if request.method == 'GET':
        print('get tasks')
        user_id = db.find_user_id(validate_login(db, session))
        data = db.session.query(db.TaskList).filter(db.TaskList.userID == user_id,
                                                    db.TaskList.completed == False).all()

        _data = parseSAtoJson(data)
        return jsonify(data=_data)


'''
@app.route('/update_tasks', methods=['GET', 'POST'])
def update_tasks():
    data = request.get_json()

    target = session.query(db.TaskList).filter(db.TaskList.todoID == data['todoID']).first()

    target.title = data['title']  # if not None else ''
    target.requestTo = data['requestTo']
    target.requestFrom = data['requestFrom']
    target.formID = data['formID']
    target.attachment = data['attachment']
    target.taskStatus = data['taskStatus']
    target.completed = data['completed']
    target.comment = data['comment']
    target.schedule = data['schedule'] if data['schedule'] == datetime else None

    session.commit()
    return jsonify(data='')


@app.route('/add_tasks', methods=['GET', 'POST'])
def add_tasks():
    if request.method == 'POST':
        try:
            print('add_my_request')
            data = request.get_json()
            username = validate_login(db, session)
            user_id = db.find_user_id(username)

            data['userID'] = user_id
            data['title'] = data['title']  # if not None else ''
            data['requestTo'] = db.find_username(user_id) if data['requestTo'] != username else username
            data['requestFrom'] = db.find_username(user_id) if data['requestFrom'] != username else username
            data['formID'] = data['formID']
            data['attachment'] = data['attachment']
            data['taskStatus'] = data['taskStatus']
            data['completed'] = data['completed']
            data['comment'] = data['comment']
            print('-----dic-----')
            data = db.TaskList(**data)

            session.add(data)
            print('-----add-----')
            session.commit()
            return jsonify(data='posted completed')

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return jsonify(data='error')

'''
