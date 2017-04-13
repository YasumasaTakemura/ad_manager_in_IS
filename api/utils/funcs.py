from datetime import datetime
from flask import request, jsonify
import jwt
import json
import csv
import re
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta


##########################################
# Datetime
##########################################

def today():
    return date.today()

def yesterday():
    return date.today() - timedelta(days=1)

def days_later(num):
    return today + relativedelta(days= num)

def months_later(num):
    return today + relativedelta(months= num)

def years_later(num):
    return today + relativedelta(years= num)

def begging_of_month():
    today = date.today()
    return today - timedelta(days=today.day-1)

def end_of_month(num=1):

    today = date.today()
    return today + relativedelta(months=num) - timedelta(days=today.day)


##########################################
# CASTER
##########################################
def num_caster(num):
    try:
        return int(num)
    except Exception:
        number = num.replace('%', '').replace('％','').replace(',', '').replace('¥', '').replace('￥', '').replace('$', '').replace('＄','')
        if number in ['0', '-', 'n/a']:
            return 0

    # validate including period in number
    if len(number.split('.')) > 1:
        # check float or not
        if int(number.split('.')[-1]) > 0:
            return float(number)
        return int(number.split('.')[0])

    # no period in number
    return int(number.split('.')[-1])


def date_caster(_datetime):
    dt = re.findall(r'\d+', _datetime)
    return '-'.join([dt[0], dt[1], dt[-1]])

def int_to_str(data, target):
    temp = []
    for row in data:
        for k, v  in row.items():
            if isinstance(v , int ) and k != target:
                row.update({k:str(v)})
                temp.append(row)
    return temp

def str_to_int(data):
    for row in data:
        for item in row:

            if item == 'impressions':
                row['impressions'] = int(row['impressions'])

            if item == 'clicks':
                row['clicks'] = int(row['clicks'])

    return data

def cast_to_dict(data):
    temp = []
    for row in data:
        temp.append(row.export_all_data())
    return temp

def list_to_json(header ,body):
    res =[]

    for i , row in enumerate(body):
        temp ={}

        for k ,v  in row.items():
            print(k ,v)


    res.append(res)

def json_to_csv(data,header,filename):
    with open( '{}.csv'.format(filename), 'w',newline="") as f:
        w = csv.DictWriter(f, fieldnames=header,delimiter=',',lineterminator='\n')
        w.writeheader()
        w.writerows(data)

def date_to_int(dt_time):
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day

##########################################
# Detector
##########################################

def detect_device_type(kwd):
    device_type = re.findall(r'[^\_\【\】\[\]\-\@]+', kwd.lower())

    for ios in ['ios','iOS','IOS','iPhone','iphone'] :
        if ios in device_type:
            device_type = 'ios'
            return device_type


    for android in ['and', 'android','Android','ANDROID', 'And', 'AND'] :
        if android in device_type:
            device_type = 'android'
            return device_type

    if 'pc' in device_type:
        device_type = 'pc'

    else:
        device_type = 'all'

    return device_type



##########################################
# Remover
##########################################

def remove_nt(text):
    return re.findall(r'\S+', text)[0]


def remove_specified_key(data, keys):
    temp = []
    for row in data:
        temp.append({item: row[item] for item in row if item not in keys})

    return temp

##########################################
# Add
##########################################
def add_fields(data, new_key, new_val):
    temp = []
    for item in data:
        item.update({new_key: new_val})
        temp.append(item)
    return temp

def add_fields_case(data, new_key, case,func):
    temp = []
    for item in data:
        if case in item.keys():
            item.update({new_key: func(item[case])})
        temp.append(item)
    return temp

##########################################
# Replacer
##########################################
def replace_key_name(data, old, new):
    temp = []

    # type check
    if isinstance(data, list) is False: raise ValueError('must to be type:list')
    if isinstance(old, str) is False: raise ValueError('must to be type:str')
    if isinstance(new, str) is False: raise ValueError('must to be type:str')

    for item in data:
        item[new] = item.pop(old)
        temp.append(item)
    return temp

##########################################
# Pickup
##########################################
def pickup_specified_key(data, target_key, pickup_key, new_key_name):
    temp = []
    for i, row in enumerate(data):
        try:
            for item in row[target_key]:
                 if item['action_type'] == pickup_key:
                    row.update({new_key_name: item['value']})
                    temp.append(row)

        except KeyError as e:
            temp.append(row)

    return temp

##########################################
# Shaper
##########################################
def shape(data, keys):
    temp = []
    for row in data:
        _row = {}
        for k, v in row.items():
            if k not in keys:
                _row.update({k: v})
        temp.append(_row)
    return temp




# nomal function
def support_datetime_default(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()
    raise TypeError(repr(dt) + " is not JSON serializable")


def parseSAtoJson(data):

    _data = []
    for d in data:
        __data = {}
        for i in d:
            __data.update({i[0]: i[1]})
        _data.append(__data)
    return _data

#  join table with additional key
def join_table_with_additional_key(objects,key):
    _data = []

    for object in objects:  # get rows
        __data = {}
        for obj in object:  # get each key and value
            __data.update({key: object.friend.username})
            __data.update({obj[0]: obj[1]})
        _data.append(__data)
    return _data

# reshape sqlAlchemy object into dict ##
def reshape_orm_result(li_datasource):
    # Reshaper : cast {tuple to dict}
    dataset = []
    for data in li_datasource:
        temp = {}
        for i in data:
            temp.update({i[0]: i[1]})
        dataset.append(temp)

    # Reshaper : cast and lowercase
    shaped_dataset = []
    for data in dataset:
        temp_dict = {}
        for k, v in data.items():

            # cast datetime type into str type
            if isinstance(v, datetime):
                dct = {k: v.strftime('%Y/%m/%d')}
                temp_dict.update(dct)
                pass

            # cast bool to str : this is for JS
            # JS allows  only 'true or false' but 'True or Flase'
            elif isinstance(v, bool) or v == None:
                #dct = {k: str(v).lower()}
                dct = json.dumps({k: v})
                temp_dict.update({k: v})
                pass

            else:
                temp_dict.update({k: v})
        shaped_dataset.append(temp_dict)
    return shaped_dataset


def get_addon_by_groups(db,session,groups_joined):
    addon_list = []
    for g in groups_joined:

        addon = session.query(db.Addon).filter(db.Addon.group_id == g[0]).all()
        if addon:
            addon_list += reshape_orm_result(addon)
    return addon_list


def validate_login(db,session):
    # JWT secret key
    secretKey = 'secretKey'
    try:
        # pick token up in header
        # receive by json casted into dict
        data = request.headers['Authorization'].split(' ')[1]

        # check token is empty
        if data:
            token = jwt.decode(data, secretKey)
            session.rollback()
            user = session.query(db.User).filter_by(username=token['username']).first()

            # check expired
            expired = datetime.fromtimestamp(token['exp']) - datetime.now()
            if expired > timedelta():
                return user.username

            return user.username

    except TypeError as e:
        print('TypeError')
        print(e)

    except KeyError as e:
        print('KeyError')
        print(e)
        return jsonify(res={'token': '', 'username': ''}), 200

    except jwt.ExpiredSignatureError:
        print('jwt.ExpiredSignatureError')
        return jsonify(data='error')




# for save
# this class twitter Cursor class equal Generator
class Generator(object):
    """
    The ads API Client class which functions as a container for basic
    API consumer information.
    """

    def __init__(self, klass, request, **kwargs):
        self._klass = klass
        self._client = request.client
        self._method = request.method
        self._resource = request.resource

        self._options = kwargs.copy()
        self._options.update(request.options)

        self._collection = []
        self._current_index = 0
        self._next_cursor = None
        self._total_count = 0

        self.__from_response(request.perform())

    @property
    def exhausted(self):
        """
        Returns True if the custor instance is exhausted.
        """
        return False if self._next_cursor else True

    @property
    def count(self):
        """
        Returns the total number of items available to this cursor instance.
        """
        return self._total_count or len(self._collection)

    @property
    def first(self):
        """
        Returns the first item of available items available to the cursor instance.
        """
        return next(iter(self._collection), None)

    @property
    def fetched(self):
        """
        Returns the number of items fetched so far.
        """
        return len(self._collection)

    def __iter__(self):
        return self

    def next(self):
        """Returns the next item in the cursor."""
        if self._current_index < len(self._collection):
            value = self._collection[self._current_index]
            self._current_index += 1
            return value
        elif self._next_cursor:
            self.__fetch_next()
            return self.next()
        else:
            self._current_index = 0
            raise StopIteration

    __next__ = next

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #self.__die()
        pass

    def __fetch_next(self):
        options = self._options.copy()
        params = options.get('params', {})
        params.update({'cursor': self._next_cursor})
        options['params'] = params
        #response = Request(self._client, self._method, self._resource, **options).perform()
        #return self.__from_response(response)

    def __from_response(self, response):
        self._next_cursor = response.body.get('next_cursor', None)
        if 'total_count' in response.body:
            self._total_count = int(response.body['total_count'])

        for item in response.body['data']:
            if 'from_response' in dir(self._klass):
                init_with = self._options.get('init_with', None)
                obj = self._klass(*init_with) if init_with else self._klass()
                self._collection.append(obj.from_response(item))
            else:
                self._collection.append(item)