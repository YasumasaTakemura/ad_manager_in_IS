#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result, parseSAtoJson
from db.admin import admin
from flask_cors import CORS, cross_origin
from flask import redirect, request, jsonify
from flask import Blueprint
from sqlalchemy import delete, asc, desc, or_
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
import json
from datetime import datetime
import jwt
from datetime import *

# bind db connection
session = admin.session

# ----------------------- #
# BluePrint
# ----------------------- #
# crate blueprint instance
app = Blueprint('tasks', __name__)


# ----------------------- #
# CORS
# ----------------------- #
# CORS(app, resources={r"/*": {"origins": "*"}})

# ----------------------- #
# function
# ----------------------- #
def get_comment():
    user_id = admin.find_user_id(validate_login(admin, session))
    data = admin.session.query(admin.CommentForTasks).filter(admin.CommentForTasks.userID == user_id).order_by(
        admin.CommentForTasks.id).all()
    data = parseSAtoJson(data)
    return data


def get_schedule():
    user_id = admin.find_user_id(validate_login(admin, session))
    data = admin.session.query(admin.ScheduleForTasks).filter(admin.ScheduleForTasks.userID == user_id).order_by(
        admin.ScheduleForTasks.id).all()
    data = parseSAtoJson(data)
    return data


def get_attachment():
    user_id = admin.find_user_id(validate_login(admin, session))
    data = admin.session.query(admin.AttachmentForTasks).filter(admin.AttachmentForTasks.userID == user_id).order_by(
        admin.AttachmentForTasks.id).all()
    data = parseSAtoJson(data)
    return data


def get_forms():
    user_id = admin.find_user_id(validate_login(admin, session))
    data = admin.session.query(admin.FormsForTasks).filter(admin.FormsForTasks.userID == user_id).order_by(
        admin.FormsForTasks.id).all()
    data = parseSAtoJson(data)
    return data


def join_tables(tasks, table , key):
    for task in tasks:
        arr=[]
        for c in table:
            if c['todoID'] == task['todoID']:
                arr.append(c)
        task[key] = arr


def get_my_tasks():
    username = validate_login(admin, session)
    user_id = admin.find_user_id(validate_login(admin, session))

    data = admin.session.query(admin.TaskList).filter(
        or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
        admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()

    data = parseSAtoJson(data)
    comment = get_comment()
    schedule = get_schedule()
    attachment = get_attachment()
    forms = get_forms()

    '''
    # join comment on tasks
    # comparing data and comment array and matches todoID
    for d in data:
        comments=[]
        for c in comment:
            if c['todoID'] == d['todoID']:
                comments.append(c)
        d['comment'] = comments

    '''
    join_tables(data, comment, 'comment')
    join_tables(data, schedule, 'schedule')
    join_tables(data, attachment, 'attachment')
    join_tables(data, forms, 'forms')
    print(data)

    '''# join scheduler on tasks
    for d in data:
        comments=[]
        for c in comment:
            if c['todoID'] == d['todoID']:
                comments.append(c)
        d['schedule'] = comments



    # join attachment on tasks
    for d in data:
        comments=[]
        for c in comment:
            if c['todoID'] == d['todoID']:
                comments.append(c)
        d['attachment'] = comments

    # join forms on tasks
    for d in data:
        comments=[]
        for c in comment:
            if c['todoID'] == d['todoID']:
                comments.append(c)
        d['forms'] = comments
    '''

    return data


# ----------------------- #
# Task Lists
# ----------------------- #


@app.route('/get_tasks', methods=['GET', 'POST'])
def get_tasks():
    if request.method == 'GET':
        print('get tasks')
        username = validate_login(admin, session)
        user_id = admin.find_user_id(validate_login(admin, session))

        data = admin.session.query(admin.TaskList).filter(
            or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
            admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()

        data = parseSAtoJson(data)
        comment = get_comment()

        # join comment on tasks
        # comparing data and comment array and matches todoID
        for d in data:
            for c in comment:
                if c['todoID'] == d['todoID']:
                    d['comment'] = comment

        return jsonify(data= get_my_tasks())


@app.route('/get_all_tasks', methods=['GET', 'POST'])
def get_all_tasks():
    if request.method == 'GET':
        print('get tasks')
        user_id = admin.find_user_id(validate_login(admin, session))
        data = admin.session.query(admin.TaskList).filter(admin.TaskList.userID == user_id).order_by(admin.TaskList.todoID).all()

        _data = parseSAtoJson(data)
        return jsonify(data=_data)


@app.route('/update_tasks', methods=['GET', 'POST'])
def update_tasks():
    username = validate_login(admin, session)
    user_id = admin.find_user_id(username)
    data = request.get_json()['task']
    print(data)
    data['requestTo'] = request.get_json()['to']
    target = session.query(admin.TaskList).filter(admin.TaskList.todoID == data['todoID']).first()

    # ----------------------- #
    # change taskStatus
    # ----------------------- #
    req = ''
    if data['requestTo'] != username and data['requestFrom'] == username:
        req = 'push'
    elif data['requestTo'] == username and data['requestFrom'] != username:
        req = 'pull'
    elif data['requestTo'] == username and data['requestFrom'] == username:
        req = 'self'

    # ----------------------- #
    # update each columns
    # ----------------------- #

    target.title = data['title']  # if not None else ''
    target.requestTo = data['requestTo']
    target.requestFrom = data['requestFrom']
    target.formID = data['formID']
    target.attachment = data['attachment']
    target.taskStatus = req
    target.completed = data['completed']
    #target.comment = data['comment']
    target.committed = data['committed']
    target.schedule = data['schedule'] if data['schedule'] == datetime else None

    session.commit()
    data = admin.session.query(admin.TaskList).filter(or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
                                                admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()
    data = parseSAtoJson(data)
    return jsonify(data=data)


@app.route('/add_tasks', methods=['GET', 'POST'])
def add_tasks():
    if request.method == 'POST':
        try:
            print('add_my_request')
            print('-----')

            title = request.get_json()['title']
            # print(data)
            username = validate_login(admin, session)
            user_id = admin.find_user_id(username)
            print(title)

            data = {}

            data['userID'] = user_id
            data['title'] = title  # if not None else ''
            data['requestTo'] = username
            data['requestFrom'] = username

            print('-----dic-----')
            print(data)
            print(dict(data))
            data = admin.TaskList(**data)

            session.add(data)
            print('-----add-----')
            session.commit()
            data = admin.session.query(admin.TaskList).filter(
                or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
                admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()
            data = parseSAtoJson(data)
            return jsonify(data=data)

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return jsonify(data='posted completed')


@app.route('/copy_tasks', methods=['GET', 'POST'])
def copy_tasks():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # omit todoID from original task
            data.pop('todoID', None)
            username = validate_login(admin, session)
            user_id = admin.find_user_id(username)

            # ----------------------- #
            # change taskStatus
            # ----------------------- #
            req = ''
            if data['requestTo'] != username and data['requestFrom'] == username:
                req = 'push'
            elif data['requestTo'] == username and data['requestFrom'] != username:
                req = 'pull'
            elif data['requestTo'] == username and data['requestFrom'] == username:
                req = 'self'

            data['taskStatus'] = req
            data = admin.TaskList(**data)

            session.add(data)
            session.commit()
            data = admin.session.query(admin.TaskList).filter(
                or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
                admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()
            data = parseSAtoJson(data)
            return jsonify(data=data)

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return jsonify(data='posted completed')


@app.route('/delete_tasks', methods=['GET', 'POST'])
def delete_tasks_tasks():
    try:
        username = validate_login(admin, session)
        user_id = admin.find_user_id(username)
        data = request.get_json()
        # data['requestTo'] = request.get_json()['to']

        print('------data--------')
        print(data)
        print(data['todoID'])
        print(data['requestFrom'])

        target = session.query(admin.TaskList).filter(admin.TaskList.todoID == data['todoID']).first()
        print(target.todoID)
        session.delete(target)
        session.commit()

        data = admin.session.query(admin.TaskList).filter(
            or_(admin.TaskList.requestTo == username, admin.TaskList.userID == user_id),
            admin.TaskList.completed == False).order_by(admin.TaskList.todoID).all()
        data = parseSAtoJson(data)
        return jsonify(data=data)

    except SQLAlchemyError as e:
        print(e)
        # session.rollback()
        return jsonify(data=e)


@app.route('/get_comments', methods=['GET', 'POST'])
def get_comments():
    if request.method == 'GET':
        print('get_comments')
        user_id = admin.find_user_id(validate_login(admin, session))
        data = admin.session.query(admin.CommentForTasks).filter(admin.CommentForTasks.userID == user_id).all()
        data = parseSAtoJson(data)
        print(data)
        return jsonify(data=data)


@app.route('/add_comments', methods=['GET', 'POST'])
def add_comments():
    if request.method == 'POST':
        try:
            print('add_comment')
            data = request.get_json()
            username = validate_login(admin, session)
            user_id = admin.find_user_id(username)

            data['username'] = admin.find_username(data['userID'])
            data = admin.CommentForTasks(**data)
            session.add(data)
            session.commit()
            data = get_my_tasks()
            return jsonify(data=data)

        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            return jsonify(data='posted completed')


@app.route('/update_comments', methods=['GET', 'POST'])
def update_comments():
    username = validate_login(admin, session)
    user_id = admin.find_user_id(username)
    data = request.get_json()
    print(data)
    target = session.query(admin.CommentForTasks).filter(admin.CommentForTasks.id == data['id']).first()
    print(target)
    target.comments = data['comments']

    # ----------------------- #
    # update each columns
    # ----------------------- #
    # target.comments = data['comments']  # if not None else ''
    session.commit()
    data = get_my_tasks()
    print(data)
    return jsonify(data=data)
