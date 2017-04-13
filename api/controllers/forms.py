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
app = Blueprint('forms', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# requests
###########################

@app.route('/get_template_list', methods=['GET', 'POST'])
def get_template_list():
    if request.method == 'GET':
        print('get_template_list')
        user_id = db.find_user_id(validate_login(db,session))
        print(user_id)
        data = session.query(db.FormTemplate).filter(db.FormTemplate.manager_id == user_id).all()
        data=reshape_orm_result(data)
        print(data)

        return jsonify(data=data)

@app.route('/add_templates', methods=['GET', 'POST'])
def add_templates():
    if request.method == 'POST':
        print('add_templates')
        data = request.get_json()
        user_id = db.find_user_id(validate_login(db,session))

        print(data)
        post_data ={
            'group_id':data['groupID'],
            'manager_id':user_id,
            'addon_name':data['addonName'],
            'addon_id':data['addonID'],

        }

        session.add(db.Addon(**post_data))
        session.commit()
        #data = session.query(db.FormTemplate).filter(db.FormTemplate.manager_id == user_id).all()
        #data=reshape_orm_result(data)
        #print(data)
        return jsonify(data=data)

