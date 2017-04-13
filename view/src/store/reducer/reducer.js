/**
 * Created by YasumasaTakemura on 2017/03/31.
 */

import * as types from '../actions/actions'
import React, {Component} from 'react'
import _ from 'lodash'
import {ValidateEmpty, today, yesterday} from '../../utils/funcs'

export function Report(state = {data: [], header: []}, action) {
    switch (action.type) {

        case types.PUSHREPORT:
            let noTypeInAction = _.omit(action, ['type']);
            console.log('-----push report!-----');
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}
export function FilteredDatasets(state = {data: []}, action) {
    switch (action.type) {

        case types.FILTEREDDATASETS:
            let noTypeInAction = _.omit(action, ['type']);
            console.log('-----push report!-----');
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}
export function Input(state = {input: ''}, action) {
    switch (action.type) {

        case types.PUSHINPUT:
            let noTypeInAction = _.omit(action, ['type']);
            console.log('-----push report!-----');
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}

let _toggle = {
    calender: false,
};

export function toggle(state = {..._toggle}, action) {
    switch (action.type) {

        case types.TOGGLE:
            let noTypeInAction = _.omit(action, ['type']);
            console.log('----- toggle !-----');
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}

let _post = {

    start_time: yesterday,
    end_time: today,
    selected: {
        account: {
            name: '-----',
            id: '',
        },
        product: {
            name: '-----',
            id: '',
        },
        media: {
            name: '-----',
            id: '',
        },
        device: {
            name: '-----',
            id:''
        },

    }


}

export function post(state = {..._post}, action) {


    switch (action.type) {

        case types.POST:
            return {
                ...state,
                start_time: action.state.start_time,
                end_time:action.state.end_time,

            };

        case types.SET_ACCOUNT:
            return {
                ...state,
                selected: {
                    ...state.selected,
                    account: {
                        ...action.state

                    }
                }
            };

        case types.SET_PRODUCT:
            let __product_params = {
                ...state,
                selected: {
                    ...state.selected,
                    product: {
                        ...action.state

                    }
                }
            };
            return {...__product_params};

        case types.SET_MEDIA:
            let __media_params = {
                ...state,
                selected: {
                    ...state.selected,
                    media: {
                        ...action.state

                    }
                }
            };
            return {...__media_params};

        case types.SET_DEVICE:
            let __device_params = {
                ...state,
                selected: {
                    ...state.selected,
                    device: {
                        ...action.state

                    }
                }
            };
            return {...__device_params};


        default:
            return state
    }
}


let _kpis = {}
export function kpis(state = {..._kpis}, action) {
    switch (action.type) {

        case types.KPIS:
            let noTypeInAction = _.omit(action, ['type']);
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}

export function selected(state = {selected: 'by_product'}, action) {
    switch (action.type) {

        case types.PUSHSELECTED:
            let noTypeInAction = _.omit(action, ['type']);
            console.log('----- toggle !-----');
            ValidateEmpty(action, state);
            return {...state, ...noTypeInAction};

        default:
            return state
    }
}


export function initializedResisterAccount(state = {}, action) {
    switch (action.type) {


        case types.INITREGISTERACCOUNT:
            return {...action.state};

        default:
            return state
    }
}


export function selectedItems(state = {}, action) {

    let selected = {
        selectedAccount: {
            name: 'choose',
            id: '',
        },
        selectedProduct: {
            name: 'choose',
            id: '',
        },
        selectedMedia: {
            name: 'choose',
            id: '',
        },
        selectedDecive: 'chooose',


    }

    switch (action.type) {

        case types.SELECTACCOUNT:
            return {...state, ...action.state};

        case types.GetAccountName:

            let account_names = []
            for (let account of state) {
                account_names.push(account.account_name)
            }

            return {state, account_names};


        default:
            return {...state}
    }
}


export function promotionList(state = {list:[]} ,action) {
    switch (action.type) {

        case types.PUSH_PROMOTION_LIST:
            return {...state, ...action.state};

        case types.UPDATE_PROMOTION_LIST:
            return {...state, ...action.state};

        default:
            return state
    }
}

