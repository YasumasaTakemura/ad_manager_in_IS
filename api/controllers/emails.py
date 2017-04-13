#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.funcs import validate_login, reshape_orm_result, parseSAtoJson
from db.admin import admin
from app import app as flask_app
from flask_cors import CORS, cross_origin
from flask import redirect, request, jsonify
from flask import Blueprint
from flask_mail import Message, Mail
from sqlalchemy import delete, asc, desc, or_
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
import json
from datetime import datetime
import jwt
from datetime import *

#bind db connection
session = admin.session

# ----------------------- #
# BluePrint
# ----------------------- #
# crate blueprint instance
app = Blueprint('email', __name__)


# ----------------------- #
# Task Lists
# ----------------------- #


@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    print('send_email')
    try:
        with flask_app.app_context():
            mail = Mail(app)
            msg = Message(sender=(u"admin", "yasumasa0708t@gmail.com"),
                          subject=u"test",
                          recipients=["yasu.0708t@gmail.com"],
                          #reply_to=u"reply <somebody@example.com>"
                          )
            msg.body = u"this is a test"
            mail.send(msg)
        return 'successed!'
    except Exception as e:
        print(e)