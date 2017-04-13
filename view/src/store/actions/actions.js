/**
 * Created by YasumasaTakemura on 2017/03/31.
 */
import {GenerateDict, ValidateEmpty} from '../../utils/funcs'
export const PUSHREPORT = 'PUSHREPORT'
export const PUSHINPUT = 'PUSHINPUT'
export const FILTEREDDATASETS = 'FILTEREDDATASETS'
export const TOGGLE = 'TOGGLE'
export const POST = 'POST'
export const KPIS = 'KPIS'
export const PUSHSELECTED = 'PUSHSELECTED'
export const INITREGISTERACCOUNT = 'INITREGISTERACCOUNT'
export const GetAccountName = 'GetAccountName'
export const SELECTACCOUNT = 'SELECTACCOUNT'
export const SELECTPRODUCT = 'SELECTPRODUCT'
export const SELECTMEDIA = 'SELECTMEDIA'
export const SELECTDEVICE = 'SELECTDEVICE'
export const SET_ACCOUNT = 'SET_ACCOUNT'
export const SET_PRODUCT = 'SET_PRODUCT'
export const SET_MEDIA = 'SET_MEDIA'
export const SET_DEVICE = 'SET_DEVICE'
export const PUSH_PROMOTION_LIST = 'PUSH_PROMOTION_LIST'
export const UPDATE_PROMOTION_LIST = 'UPDATE_PROMOTION_LIST'


export const pushReport = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: PUSHREPORT, ...state}

}

export const pushInput = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: PUSHINPUT, ...state}

}

export const pushFilteredDatasets = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: FILTEREDDATASETS, ...state}

}

export const toggle = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: TOGGLE, ...state}

}

export const post = (state) => {

    // for (let [key, value] of Object.entries(state)) {
    //   Object.assign({...state, ...GenerateDict(key, value)})
    // }

    return {type: POST, state}

}

export const storeKpis = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: KPIS, ...state}

}

export const pushSelected = (state) => {

    for (let [key, value] of Object.entries(state)) {
        Object.assign({...state, ...GenerateDict(key, value)})
    }

    return {type: PUSHSELECTED, ...state}

}

export const initRegisterAccount = (state) => {


    return {type: INITREGISTERACCOUNT, state}

}


export const getAccountName = (state) => {


    return {type: GetAccountName, state}

}

export const selectAccount = (state) => {


    return {type: SELECTACCOUNT, state}

}
export const selectProduct = (state) => {
    return {type: SELECTPRODUCT, state}

}

export const selectMedia = (state) => {
    return {type: SELECTMEDIA, state}

}

export const selectDevice = (state) => {
    return {type: SELECTDEVICE, state}

}

export const setAccount = (state) => {
    return {type: SET_ACCOUNT, state}

}

export const setProduct = (state) => {
    return {type: SET_PRODUCT, state}

}

export const setMedia = (state) => {
    return {type: SET_MEDIA, state}

}

export const setDevice = (state) => {
    return {type: SET_DEVICE, state}

}


// promotion list
export const pushPromotionList = (state) => {
    return {type: PUSH_PROMOTION_LIST, state}

}

export const update_promotion_list = (state) => {
    return {type: UPDATE_PROMOTION_LIST, state}

}

