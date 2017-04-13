#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result, parseSAtoJson
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
app = Blueprint('generals', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# Group Managing
###########################

# search users
@app.route('/search_users', methods=['GET', 'POST'])
def search_users():
    print('posted')
    current_user = validate_login(db,session)
    input_value = request.get_json()['InputValue']
    print(input_value)

    input_value = '%{}%'.format(input_value)
    print(input_value)

    if current_user:
        session.rollback()
        users = session.query(db.User).filter(db.User.username.like('%s' % input_value)).order_by(
            asc(db.User.username)).all()
        # users = session.query(db.User).filter_by(username=current_user).order_by(asc(db.User.username)).all()
        data = reshape_orm_result(users)
        print(data)
        return jsonify(data=data)

    print('error')
    return jsonify()




