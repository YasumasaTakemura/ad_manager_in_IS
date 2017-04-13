import json
import os
import os.path
import shutil
import sys
import requests
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

from urllib.parse import urlparse, urljoin, urlencode, unquote
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import feedparser
from bs4 import BeautifulSoup as bs

# bind db connection
session = admin.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('selenium', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})

###########################
# ChromeDriver config
###########################
chromeOptions = webdriver.ChromeOptions()
prefs ={'download.default_directory':'/Users/YasumasaTakemura/Desktop/'}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')

@app.route('/chrome_scraping', methods=['GET','POST'])
def chrome_scraping():
    params=request.get_json()

    driver = webdriver.Chrome(executable_path='/Users/YasumasaTakemura/Downloads/chromedriver',chrome_options=chromeOptions)
    base_url = 'https://spadvertiser.i-mobile.co.jp/'
    base_url = 'https://ms.zucksadnetwork.com/'
    base_url = 'https://www.nend.net/'
    admin_url = 'https://www.nend.net/admin/login'
    #dashboard_url = 'https://www.nend.net/a/home'
    #login_url = 'https://www.nend.net/admin/login'
    login_url = 'agent/login'
    dashboard_url = 'https://www.nend.net/a/home'
    #dashboard_url = 'https://spagency.i-mobile.co.jp/advertiser.aspx'
    report_url = 'https://spadvertiser.i-mobile.co.jp/monthly_report.aspx#'
    report_url = 'agent/325/report2/order/list'

    driver.get(admin_url)
    # print(driver.page_source)
    try:
        print(driver.page_source)
        username = driver.find_element_by_xpath('//*[@id="UserMail"]')
        password = driver.find_element_by_xpath('//*[@id="UserPass"]')
        username.send_keys('r_kase@denno-advertisement.com')
        password.send_keys('interspace9999')
        password.submit()
        #driver.get(dashboard_url)

        # access each client layer
        driver.get('https://www.nend.net/a/advertiser/login/1762')

        # access report page
        driver.get('https://www.nend.net/d/report/search')
        data =driver.page_source
        print(data)
        driver.save_screenshot('testcap.png')
        driver.find_element_by_link_text('CSVダウンロード').click()


        print('-------------------')

        driver.quit()
        return jsonify(data=data)

    except Exception as e:
        print(e)
        driver.quit()
        return jsonify(data='no data')