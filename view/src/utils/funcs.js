/**
 * Created by YasumasaTakemura on 2017/03/31.
 */
import React, {Component, PropTypes} from 'react';
import axios from 'axios'
import moment from 'moment'

export function validateNumber(num) {
        if (isFloat(num)) {
            return num.toLocaleString()
        }
        return num
    }


export  function isFloat(num) {
        if(typeof num == Number ||  num % 1 == 0) {
            return true
        } else {
            return false
        }
    }

export function isEmpty(obj) {
    var hasOwnProperty = Object.prototype.hasOwnProperty;

    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.

    if (typeof obj == Number) return false;
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;


    // if (obj === 0)  return true;

    // If it isn't an object at this point
    // it is empty, but it can't be anything *but* empty
    // Is it empty?  Depends on your application.
    if (typeof obj !== "object") return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }


    return true;
}

export function strToDate(str) {
    var options = {year: "numeric", month: "numeric", day: "numeric", weekday: "short"};
    return new Date(Date.parse(str)).toLocaleTimeString("ja-JP", options).split(' ')[0]
}

export function dateToStr(date) {
    return moment(date).format('YYYY-MM-DD')
    // var options = {year: "numeric", month: "numeric", day: "numeric"};
    // return new Date(Date.parse(str)).toLocaleTimeString("ja-JP", options).split(' ')[0]
}

export function dateToStrOnlyMonth(date) {
    return moment(date).format('YYYY-MM')
    // var options = {year: "numeric", month: "numeric", day: "numeric"};
    // return new Date(Date.parse(str)).toLocaleTimeString("ja-JP", options).split(' ')[0]
}

// Render the Calendar
export var today = new Date();
export var yesterday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1);
export var lastWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
export var lastYear = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());


export function floatFormat(number, n) {
    var _pow = Math.pow(10, n);

    return Math.round(number * _pow) / _pow;
}


export function yenFormat(num) {
    return new Intl.NumberFormat('ja-JP', {style: 'currency', currency: 'JPY'}).format(num)
}


export function percentageFormat(num) {
    return new Intl.NumberFormat('en-IN', {style: 'percent'}).format(num)
}


export function pointFormat(num) {
    return new Intl.NumberFormat().format(num)
}


export function print(any) {
    console.log(any)
}

export function GenerateDict(key, value) {
    let dict = {};
    dict[key] = value;
    return dict
}

// check the object or list is empty or not
export function ValidateEmpty(action, state) {
    for (let [key, value] of Object.entries(action)) {
        if (value.length == 0 || Object.keys(value).length == 0) {
            return state
        }
    }
}

let domain = 'http://0.0.0.0:8080/'
let api_ver = 'api/v1/'

export class CRUD {

    constructor(props) {
        this.props = props;

    }


    __initRegisterAccount() {
        let url = domain + api_ver + 'init_resister_account'

        try {
            axios.get(url).then((data)=> {
                if (data.data.data) {

                    let accounts = []
                    let products = []
                    let medias = []
                    let device = []


                    for (let dataset of data.data.data[0]) {
                        let temp_act = {}

                        for (let key in dataset) {
                            if (key == 'account_name') {
                                temp_act['account_name'] = dataset[key]
                            } else {
                                temp_act['id'] = dataset[key]
                            }
                        }
                        accounts.push(temp_act)
                    }

                    for (let dataset of data.data.data[1]) {
                        let temp_act = {}

                        for (let key in dataset) {
                            if (key == 'product_name') {
                                temp_act['product_name'] = dataset[key]
                            }

                            if (key == 'id') {
                                temp_act['id'] = dataset[key]

                            }
                        }
                        products.push(temp_act)
                    }

                    for (let dataset of data.data.data[2]) {
                        let temp_act = {}

                        for (let key in dataset) {
                            if (key == 'media_name') {
                                temp_act['media_name'] = dataset[key]
                            }

                            if (key == 'id') {
                                temp_act['id'] = dataset[key]

                            }
                        }
                        medias.push(temp_act)
                    }
                    for (let dataset of data.data.data[3]) {
                        let temp = {}

                        for (let key in dataset) {
                            console.log(key)
                            if (key == 'device') {
                                temp['device'] = dataset[key]
                            }

                            if (key == 'id') {
                                temp['id'] = dataset[key]

                            }
                        }

                        device.push(temp)
                    }

                    this.props.initRegisterAccount({
                        accounts: accounts,
                        products: products,
                        medias: medias,
                        device: device,
                    })
                }
            })
        } catch (e) {
            console.log(e);
        }
    }

    resisterPromotion() {
        var params = this.props.postParams.selected

        let account_name = params.account.name
        let account_id = params.account.id
        let product_name = params.product.name
        let product_id = params.product.id
        let media_name = params.media.name
        let media_id = params.media.id
        let device_name = params.device.name
        let device_id = params.device.id

        let __params = {
            account_name: account_name,
            account_id: account_id,
            product_name: product_name,
            product_id: product_id,
            media_name: media_name,
            media_id: media_id,
            device_name: device_name,
            device_id: device_id,

        }


        // validation
        for(let i in __params) {
            console.log(__params[i]);
            if (__params[i] === '') {
                alert('empty')
                return false
            }

        }

        let url = domain + api_ver + 'resister_promotion'

        try {
            axios.post(url, __params).then((data)=> {
                if (data.data.data == 200) {
                    this.getPromotionList();
                }
            })
        } catch (e) {
            console.log(e);
        }
    }


    getPromotionList() {

        let url = domain + api_ver + 'get_promotion_list'

        try {
            axios.get(url).then((data)=> {

                if (data.data.data) {
                    console.log(data.data.data)
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log('error')
            console.log(e);
        }

    }

    registerReportingTasks(promotion_id,params) {
        let url = domain + api_ver + 'register_reporting_tasks'

        var payload = {
            id:promotion_id,
            media_account_id:params.media_account_id,
            media_campaign_id:params.media_campaign_id,

        }



        console.log(payload)
        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                   if (data.data.data == 200) {
                    console.log(data.data.data)
                }
                }
            })
        } catch (e) {
            console.log(e);
        }

    }



    getRequest(props, endpoint) {

        let start_time;
        let end_time;

        //a cases for empty object
        if (props.postParams !== undefined) {
            start_time = dateToStr(props.postParams.start_time)
            end_time = dateToStr(props.postParams.end_time)
        }

        let url = domain + api_ver + endpoint + `?start_time=${start_time}&end_time=${end_time}`

        try {
            axios.get(url).then((data)=> {
                if (data.data.data) {

                    this.props.pushReport({
                            data: data.data.data.data,
                            header: data.data.data.header,
                        }
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }

    }

    runTaskManager(props) {

        let start_time;
        let end_time;

        //a cases for empty object
        if (props.postParams !== undefined) {
            start_time = dateToStr(props.postParams.start_time)
            end_time = dateToStr(props.postParams.end_time)
        }

        let domain = 'http://0.0.0.0:8080/'
        let api_ver = 'api/v1/'
        let url = domain + api_ver + 'run_tasks_manager' + `?start_time=${start_time}&end_time=${end_time}`

        try {
            axios.get(url).then((data)=> {
                if (data.data.data) {

                    this.props.pushReport({
                            data: data.data.data.data,
                            header: data.data.data.header,
                        }
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }

    }

    getReportWithTimeRange(props) {
        let url = domain + api_ver + 'get_daily_report_by_promotion'

        let start = dateToStr(props.postParams.start_time)
        let end = dateToStr(props.postParams.end_time)

        let payload = {
            params: {
                start_time: start,
                end_time: end,
            }

        }

        try {
            axios.get(url, payload).then((data)=> {
                if (data.data.data) {

                    props.pushReport({
                            data: data.data.data.data,
                            header: data.data.data.header,
                        }
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }


    }

    updateAdFee(item){

        let payload = {
            'id':item['fee_id'],
            'fee':parseFloat(item['fee'])
        }

        let endpoint = 'update_ad_fee'
        let url = domain + api_ver + endpoint

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }

    updateBudget(item){

        let payload = {
            'id':item['m_budget_id'],
            'budget':parseFloat(parseInt(item['m_budget']))
        }

        let endpoint = 'update_m_budget'
        let url = domain + api_ver + endpoint

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }


    updateStaff(item){

        let payload = {
            'id':item['staff_id'],
            'staff':item['staff']
        }

        let endpoint = 'update_staff'
        let url = domain + api_ver + endpoint

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }

    updateProgramId(item){

        let payload = {
            'id':item['istool_id'],
            'program_id':item['program_id']
        }

        let endpoint = 'update_program_id'
        let url = domain + api_ver + endpoint

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }

    updateProgramName(item){

        let payload = {
            'id':item['istool_id'],
            'program_name':item['program_name']
        }

        let endpoint = 'update_program_name'
        let url = domain + api_ver + endpoint

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }


    updatePromotionList(payload){
        let url = domain + api_ver + 'update_promotion_list'

        try {
            axios.post(url,payload).then((data)=> {
                if (data.data.data) {
                    this.props.pushPromotionList(
                        {list: data.data.data,}
                    )
                }
            })
        } catch (e) {
            console.log(e);
        }
    }

}
