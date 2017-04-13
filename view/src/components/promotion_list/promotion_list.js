/**
 * Created by YasumasaTakemura on 2017/04/08.
 */

import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import JsonTable from 'react-json-table';
import {Table, Thead, Th, Tr, Td} from 'reactable'
import SearchInput, {createFilter} from 'react-search-input'
import chunk from 'chunk'
import _ from 'lodash'
import {Calender} from '../../components/calender/calender'
import {yenFormat, floatFormat, pointFormat, percentageFormat, dateToStrOnlyMonth, validateNumber, isFloat} from '../../utils/funcs'
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import '../../index.css'
const array = require("array-extended");

export class PromotionList extends Component {

    state = {
        toggle_index: '',

        toggle_program_name: false,
        toggle_program_id: false,
        toggle_fee: false,
        toggle_m_budget: false,
        toggle_month: false,
        toggle_staff: false,

        input_program_name: '',
        input_program_id: '',
        input_fee: '',
        input_budget: '',
        input_staff_name: '',

    }


    componentWillMount() {
        let crud = new CRUD(this.props)
        crud.getPromotionList()

    }

    changeState(key, index) {

        this.setState({toggle_index: index})
        if (key == 'toggle_program_name') this.setState({toggle_program_name: !this.state.toggle_program_name})
        if (key == 'toggle_program_id')this.setState({toggle_program_id: !this.state.toggle_program_id})
        if (key == 'toggle_fee')this.setState({toggle_fee: !this.state.toggle_fee})
        if (key == 'toggle_m_budget')this.setState({toggle_m_budget: !this.state.toggle_m_budget})
        if (key == 'toggle_staff')this.setState({toggle_staff: !this.state.toggle_staff})

    }

    // post edited input
    postUpdateInput(item, key) {
        let crud = new CRUD(this.props)

        console.log(item, key)
        if (key == 'fee') {
            crud.updateAdFee(item)
            this.setState({toggle_fee: false})
        }

        if (key == 'm_budget') {
            crud.updateBudget(item)
            this.setState({toggle_m_budget: false})
        }


        if (key == 'staff') {
            crud.updateStaff(item)
            this.setState({toggle_staff: false})
        }


        if (key == 'program_name') {
            crud.updateProgramName(item)
            this.setState({toggle_program_name: false})
        }


        if (key == 'program_id') {
            crud.updateProgramId(item)
            this.setState({toggle_program_id: false})
        }
    }

    // update input text
    updateInput(v, index, key) {
        let target = _.find(this.props.promotionList, (item, i)=> index == i)
        target[key] = v
        for (let i in this.props.promotionList) {
            if (i == index) this.props.promotionList[i] = target
        }
        this.props.update_promotion_list({list: this.props.promotionList})
    }



    //render input depending on key and index of promotion list
    renderInput(item, index, key) {
        return this.state['toggle_' + key] && this.state.toggle_index == index ?
            <div className="render-input">
                <input onChange={(e)=>this.updateInput(e.target.value, index, key)} defaultValue={item[key]}/>
                <button onClick={()=>this.postUpdateInput(item, key)}>+</button>
            </div> : validateNumber(item[key])
    }

    renderPromotionlist() {
        return this.props.promotionList.map((item, index) => {
                return (
                    <tr className="" key={index}>


                        <td className="program"><input type="checkbox"/></td>
                        <td className="program">
                            <div onDoubleClick={()=>this.changeState('toggle_program_name', index)}
                                 className="program_name">{this.renderInput(item, index, 'program_name')}</div>
                            <div onDoubleClick={()=>this.changeState('toggle_program_id', index)}
                                 className="program_id">{this.renderInput(item, index, 'program_id')}</div>
                        </td>


                        <td className="account_name">{item.account_name}</td>
                        <td className="product_name">{item.product_name}</td>
                        <td className="media_name">{item.media_name}</td>
                        <td className="device_name">{item.device}</td>
                        <td onDoubleClick={()=>this.changeState('toggle_fee', index)}
                            className="fee">{this.renderInput(item, index, 'fee')}</td>
                        <td className="month">{dateToStrOnlyMonth(this.renderInput(item, index, 'month'))}</td>
                        <td onDoubleClick={()=>this.changeState('toggle_m_budget', index)}
                            className="budget">{this.renderInput(item, index, 'm_budget')}</td>
                        <td onDoubleClick={()=>this.changeState('toggle_staff', index)}
                            className="staff_name">{this.renderInput(item, index, 'staff')}</td>
                         <td className="spend">{validateNumber(item.spend)}</td>

                    </tr>
                )
            }
        )
    }

    render() {
        return (
            <div className="promotion-list">
                <div>Promotion List</div>
                <table className="">
                    <thead className="">
                    <tr className="">

                        <th className=""></th>
                        <th className="">プログラム</th>
                        <th className="">アカウント</th>
                        <th className="">商品名</th>
                        <th className="">メディア</th>
                        <th className="">デバイス</th>
                        <th className="">手数料</th>
                        <th className="">月</th>
                        <th className="">月予算</th>
                        <th className="">担当者</th>
                        <th className="">広告費</th>

                    </tr>
                    </thead>

                    <tbody className="">
                    {this.renderPromotionlist()}
                    </tbody>
                </table>

            </div>
        )


    }
}