/**
 * Created by YasumasaTakemura on 2017/03/31.
 */
import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as action from './actions/actions'

import {TopPage} from '../components/top/top'
import {PromotionList} from '../components/promotion_list/promotion_list'
import {RegisterPage} from '../containers/register/register'
import {Calender} from '../components/calender/calender'
import {ReportTable} from '../containers/report/report'
import ToggleManager from '../containers/toggleManager/toggleManager'


const mapStateToProps = (state)=> {

    return {
        reportDataSets: state.Report,
        filteredDatasets: state.FilteredDatasets,
        input: state.Input,
        toggler:state.toggle,
        postParams:state.post,
        kpis:state.kpis,
        selected:state.selected,
        initializedResisterAccount:state.initializedResisterAccount,
        selectedItems:state.selectedItems,
        promotionList:state.promotionList.list,
        getInput:state.getInput,

    }
}

const mapDispatchToProps = (dispatch)=> {

    return bindActionCreators({
        pushReport: action.pushReport,
        pushFilteredDatasets: action.pushFilteredDatasets,
        pushInput: action.pushInput,
        toggle: action.toggle,
        post: action.post,
        storeKpis: action.storeKpis,
        pushSelected: action.pushSelected,
        initRegisterAccount: action.initRegisterAccount,
        selectAccount: action.selectAccount,
        selectProduct: action.selectProduct,
        selectMedia: action.selectMedia,
        selectDevice: action.selectDevice,
        setAccount: action.setAccount,
        setProduct: action.setProduct,
        setMedia: action.setMedia,
        setDevice: action.setDevice,
        pushPromotionList: action.pushPromotionList,
        update_promotion_list: action.update_promotion_list,

    }, dispatch)
}
export const _TopPage= connect(mapStateToProps, mapDispatchToProps)(TopPage);
export const _ReportTable = connect(mapStateToProps, mapDispatchToProps)(ReportTable);
export const _ToggleManager = connect(mapStateToProps, mapDispatchToProps)(ToggleManager);
export const _RegisterPage = connect(mapStateToProps, mapDispatchToProps)(RegisterPage);
export const _PromotionList = connect(mapStateToProps, mapDispatchToProps)(PromotionList);



