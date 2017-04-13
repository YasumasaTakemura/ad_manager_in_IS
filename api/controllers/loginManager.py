#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
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

# JWT secret key
secretKey = 'secretKey'

###########################
# BluePrint
###########################
# register Blueprint
# set filename of controller file and register into blueprint
app = Blueprint('loginManager', __name__)
###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})

# for SqlAlchemy connection
session = admin.session

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})

# api to get username
@app.route('/getUsername', methods=['GET', 'POST'])
def getUsername():
    user_id = request.get_json()['userID']
    print(db.find_username(user_id))
    return jsonify(data = db.find_username(user_id))


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        data = request.get_json()  # recieve by json
        print(data)
        # data = request.headers['Authorization'].split(' ')[1]  # receive by json casted into dict
        # token = jwt.decode(data, secretKey)
        session.rollback()

        username = data['username']
        password = data['password']

        session.rollback()
        user = session.query(db.User).filter(db.User.username == username).first()
        user_id = db.find_user_id(user)

        if user.password == password:
            payload = {'username': username, 'exp': datetime.now() + timedelta(days=3)}
            token = jwt.encode(payload, secretKey, algorithm='HS256')

            return jsonify(res={'token': token, 'username': username, 'userID': user.user_id}), 200

        return jsonify(res=''), 200

    else:
        return jsonify(res=''), 200


@app.route('/loggin', methods=['GET', 'POST'])
def loggin():
    try:
        data = request.headers['Authorization'].split(' ')[1]  # receive by json casted into dict

        # check token is empty
        if data:
            token = jwt.decode(data, secretKey)
            session.rollback()
            user = session.query(db.User).filter_by(username=token['username']).first()
            user_id = db.find_user_id(user)
            # check expired
            expired = datetime.fromtimestamp(token['exp']) - datetime.now()

            if expired > timedelta():
                return jsonify(res={'token': data, 'username': user.username, 'userID': user.user_id}), 200
            return jsonify(res='expired'), 200

    except TypeError as e:
        print(e)
        return jsonify(res='typeerror'), 200

    except KeyError as e:
        print(e)
        return jsonify(res='keyerror'), 200

    except jwt.ExpiredSignatureError:
        return jsonify(res='jwt'), 200
