#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result, parseSAtoJson, \
    join_table_with_additional_key
from db.admin import admin
from flask_cors import CORS, cross_origin
from flask import redirect, request, render_template, url_for, jsonify
from flask import Blueprint
from sqlalchemy import delete, asc, desc, or_, alias
from sqlalchemy.orm import aliased
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
app = Blueprint('userManager', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# Group Managing
###########################

# search users
@app.route('/invite_for_friend', methods=['GET', 'POST'])
def invite_for_friend():
    print('posted')
    username = validate_login(db, session)
    user_id = db.find_user_id(username)
    print(request.get_json())
    friend_id = request.get_json()['user_id']

    try:
        relation = session.query(db.Friend).filter(db.Friend.my_id == user_id, db.Friend.friend_id == friend_id).first()
        print(relation.status)

        if relation.status == 'inviting':
            return jsonify(data='already invited')
        elif relation.status == 'friend':
            return jsonify(data='already friend')
    except:

        friend = {
            'my_id': user_id,
            'friend_id': friend_id
        }

        print(friend)
        friend = db.Friend(**friend)

        session.add(friend)
        session.commit()
        return jsonify(data='invited!')


@app.route('/be_a_friend_or_not', methods=['GET', 'POST'])
def be_a_friend_or_not():
    print(request.get_json())
    username = validate_login(db, session)
    user_id = db.find_user_id(username)
    friend_id = request.get_json()['friend_id']

    relation = session.query(db.Friend).filter(db.Friend.my_id == user_id, db.Friend.friend_id == friend_id,).first()

    if request.get_json()['answer'] == 'approve':
        relation.status = 'friend'
        session.commit()
        return jsonify(data='became a friend')

    else:
        relation.status = 'declined'
        session.commit()
        return jsonify(data='declined')


# get friends list
@app.route('/get_friends', methods=['GET', 'POST'])
def get_friends():
    user_id = db.find_user_id(validate_login(db, session))
    friends = session.query(db.Friend).join(db.Friend.user).filter(db.Friend.my_id == user_id).all()
    print(join_table_with_additional_key(friends, 'friends'))
    return jsonify(data=join_table_with_additional_key(friends, 'friends'))

###########################
# user settting
###########################


@app.route('/add_user_setting', methods=['GET', 'POST'])
def add_user_setting():
    print('posted')
    username = validate_login(db, session)
    user_id = db.find_user_id(username)
    print(request.get_json())
    friend_id = request.get_json()['user_id']

    try:
        relation = session.query(db.Friend).filter(db.Friend.my_id == user_id, db.Friend.friend_id == friend_id).first()
        print(relation.status)

        if relation.status == 'inviting':
            return jsonify(data='already invited')
        elif relation.status == 'friend':
            return jsonify(data='already friend')
    except:

        friend = {
            'my_id': user_id,
            'friend_id': friend_id
        }

        print(friend)
        friend = db.Friend(**friend)

        session.add(friend)
        session.commit()
        return jsonify(data='invited!')