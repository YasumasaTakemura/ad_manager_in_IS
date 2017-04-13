#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result
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
app = Blueprint('requests', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# requests
###########################

@app.route('/add_my_request', methods=['GET', 'POST'])
def add_my_request():
    if request.method == 'POST':
        print('add_my_request')
        print('-----')
        tasks = request.get_json()
        print(tasks)
        dic = {}
        user_id = db.find_user_id(validate_login(db,session))
        print(user_id)
        print('-----dic-----')

        dic['userID'] = user_id
        dic['title'] = tasks['taskTitle'] #if not None else ''
        dic['requestTo'] = tasks['requestTo']
        dic['requestFrom'] = user_id
        dic['form'] = tasks['form']
        dic['attachment'] = tasks['attachment']
        dic['taskStatus'] = tasks['taskStatus']
        dic['completed'] = tasks['completed']
        dic['comment'] = tasks['comment']
        print('-----dic-----')
        print(dic)
        data =db.TaskList(dict)

        session.add(data)
        session.commit()

        return jsonify(data='posted completed')
