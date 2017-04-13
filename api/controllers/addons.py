from utils.funcs import validate_login, get_addon_by_groups, reshape_orm_result
from db.admin import admin
from flask_cors import CORS, cross_origin
from flask import request,jsonify
from flask import Blueprint

from selenium import webdriver
# bind db connection
session = admin.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('addons', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# requests
###########################

@app.route('/get_my_addon', methods=['GET', 'POST'])
def get_my_addon():
    if request.method == 'GET':
        print('get_my_addon')
        user_id = admin.find_user_id(validate_login(admin, session))
        groups_joined = admin.find_group_id(user_id)

        data = get_addon_by_groups(admin, session, groups_joined)
        print(type(data))

        return jsonify(data=data)


###########################
# ChromeDriver config
###########################
chromeOptions = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/YasumasaTakemura/Desktop/'}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument(
    '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36')


@app.route('/site_manipulator', methods=['GET', 'POST'])
def chrome_scraping():
    driver = webdriver.Chrome(executable_path='/Users/YasumasaTakemura/Downloads/chromedriver',
                              chrome_options=chromeOptions)
    params = request.get_json()
    base_url = params['baseUrl']
    admin_url = params['adminUrl']
    urls = params['url']
    username = params['uername']
    password = params['password']
    username_xpath = params['uernameXpath']
    password_xpath = params['passwordXpath']

    driver.get(admin_url)
    # print(driver.page_source)
    try:
        print(driver.page_source)
        username = driver.find_element_by_xpath(username_xpath)
        password = driver.find_element_by_xpath(password_xpath)
        username.send_keys(username)
        password.send_keys(password)
        password.submit()

        actions =['','','','']

        # access each client layer

        # access base url
        driver.get(base_url)

        #deal orders
        # order include k: action name and v : params name
        for order in params['orders']:
            my_order = {}
            action=''
            for k, v in order.itmes():
                if k == 'url':
                    driver.get(v)
                elif k == 'screenShot':
                    driver.save_screenshot(v)
                elif k == 'findElement':
                    action = driver.find_element_by_link_text(v)
                elif k == 'click':
                    action.click()

        print('-------------------')

        driver.quit()
        return jsonify(data='successed')

    except Exception as e:
        print(e)
        driver.quit()
        return jsonify(data='no data')
