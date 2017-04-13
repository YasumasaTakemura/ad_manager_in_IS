/**
 * Created by YasumasaTakemura on 2017/04/09.
 */
/**
 * Created by YasumasaTakemura on 2017/04/05.
 */

import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import JsonTable from 'react-json-table';
import {Table, Thead, Th, Tr, Td} from 'reactable'
import SearchInput, {createFilter} from 'react-search-input'
import chunk from 'chunk'
import {Calender} from '../../components/calender/calender'
import {yenFormat, floatFormat, pointFormat, percentageFormat, strToDate, dateToStr, isEmpty} from '../../utils/funcs'
const array = require("array-extended");
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import '../../index.css'
import {PromotionRender} from '../../components/register/promotion'
import {MediaIDsRender} from '../../components/register/media_ids'

export class RegisterPage extends Component {
    constructor(props) {
        super(props);
        this.props = props
        this.state = {
            account: false,
            product: false,
            load: true,
            selected_promotion: [],
            params: {}

        }
    }

    componentWillMount() {
        let crud = new CRUD(this.props)
        crud.__initRegisterAccount()
        crud.getPromotionList()

    }
    render() {

        return (
            <div className="resister frame">

                <div className="switch-register-btn">
                    <button onClick={()=>this.setState({load: true})}>promotion</button>
                    <button onClick={()=>this.setState({load: false})}>media_ids</button>
                </div>

                {
                    this.state.load ? <PromotionRender {...this.props}/>: <MediaIDsRender {...this.props}/>
                }
            </div>
        )
    }

}


