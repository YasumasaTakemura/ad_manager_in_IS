#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
# from flask.ext.cors import CORS
import os
from controllers import ads


# JWT secret key
secretKey = 'secretKey'

"""
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgres://YasumasaTakemura@localhost:5432/postgres'
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"
app.config['JSON_AS_ASCII'] = False

###########################
# BluePrint
###########################
# register Blueprint
# set filename of controller file and register into blueprint
modules = [ads.app]

for module in modules:
    app.register_blueprint(module)

###########################
# CORS
###########################
# CORS(app, resources={r"/*": {"origins": "*"}})
#
# with app.test_request_context():
#     input = ['account', 'service', 'user_id', 'todo_id', 'todo_name', 'account', 'service', 'finished', 'deadline',
#              'problems', 'status_now', 'status_future', 'actions']
#
#


if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0', port=8080, debug=True,processes=3)
