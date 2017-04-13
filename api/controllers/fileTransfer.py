import json
import os
import os.path
import shutil
import sys
from datetime import *
from utils.funcs import validate_login, reshape_orm_result
from flask_cors import CORS, cross_origin
from flask import redirect, request, render_template, url_for, jsonify, current_app
from flask import Blueprint

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, InvalidRequestError, SQLAlchemyError
from sqlalchemy import asc, desc
from db.admin import admin
import dropbox

# bind db connection
session = admin.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('fileTransfer', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})

###########################
# dropbox
###########################
access_token = 'MVLwe1m2rh4AAAAAAAANFeIxtsKy6d-FH44YXCiG-ev0niHSMJYeaeMh4YJGCWXv'
dbx = dropbox.Dropbox(access_token)


def upload(dbx, folder, filename, files_object, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = '/%s/%s' % (folder, filename)

    # validator
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    # mtime = os.path.getmtime(fullname)
    try:
        res = dbx.files_upload(
            files_object, path, mode,
            # client_modified=datetime.now(),
            mute=True)
    except dropbox.exceptions.ApiError as err:
        print('*** API error', err)
        return None
    print('uploaded as', res.name.encode('utf8'))
    return res


def download(dbx, folder, filename):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s' % (folder, filename)
    while '//' in path:
        path = path.replace('//', '/')

    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        dbx.users_get_current_account()
        if 'qqfilename' not in request.form:
            print('No file part')
            return jsonify(request.url)

        filename = request.form['qqfilename']
        files_object = request.files['qqfile']

        upload(dbx, 'storage', filename, files_object)
        download(dbx, 'storage', filename,)
        print('done')
        return jsonify(data='successed')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        filename = request.get_json().filename
        data = download(dbx, 'storage', filename, )
        print('done')
        return jsonify(data= data )