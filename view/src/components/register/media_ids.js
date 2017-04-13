/**
 * Created by YasumasaTakemura on 2017/04/09.
 */

import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import JsonTable from 'react-json-table';
import {Table, Thead, Th, Tr, Td} from 'reactable'
const array = require("array-extended");
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import '../../index.css'
import {isEmpty} from '../../utils/funcs'

export class MediaIDsRender extends Component {
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

    ////////////////////////////////////////
    // resister media_ids
    ////////////////////////////////////////
    resisterMediaIDs(e) {
        e.preventDefault()
        let crud = new CRUD(this.props)
        let res = crud.resisterPromotion()
        if (res) alert('new promotion have just registered!')

    }

    selectPromotion(item) {
        console.log(item)
        this.setState({selected_promotion: [item.promotion_id, item.account_name, item.product_name, item.media_name, item.device]})
    }

    renderPromotionlist() {
        return this.props.promotionList.map((item, index) => {
                return <tr onClick={()=>this.selectPromotion(item)} className="" key={index}>
                    <td className="account_name">{item.account_name}</td>
                    <td className="product_name">{item.product_name}</td>
                    <td className="media_name">{item.media_name}</td>
                    <td className="device">{item.device}</td>

                </tr>
            }
        )
    }

    // submit task register
    registerReportingTasks(e) {
        e.preventDefault()
        let crud = new CRUD(this.props)
        console.log(this.state.selected_promotion)
        crud.registerReportingTasks(this.state.selected_promotion[0], this.state.params)

    }

    updateInput(val, type) {
        if (type == 'account_id')this.setState({
            params: {
                ...this.state.params,
                media_account_id: val
            }
        })

        if (type == 'campaign_id')this.setState({
            params: {
                ...this.state.params,
                media_campaign_id: val
            }
        })
    }

    ////////////////////////////////////////
    // Promotion
    ////////////////////////////////////////
    renderProductInput() {
        return <input onChange={(e)=>this.props.setProduct({name: e.target.value, id: 0})}
                      className="selector-child" name="account"/>
    }

    toggleProductState() {
        this.setState({product: !this.state.product})

    }

    switchProduct(key) {
        return this.state.product ? this.renderProductInput() : this.renderProductSelector();
    }

    selectProduct(v, l) {
        this.props.setProduct({
            name: l[0].label,
            id: parseInt(l[0].value)
        })
    }

    renderPromotionSelector() {
        let __temp = []
        let datasets = this.props.initializedResisterAccount
        if (!isEmpty(datasets)) {
            for (let product of datasets.products) {
                for (let key in product) {
                    if (key == 'product_name') {
                        __temp.push({value: product.id, label: product[key]})

                    }
                }
            }
        }

        return (
            <Select
                clearable={false}
                name={'product'}
                value={this.props.postParams.selected.product.name}
                options={__temp}
                onChange={(v, vl)=>this.selectProduct(v, vl)}
            />
        )
    }


    renderProduct() {
        return (
            <div className="product">
                <div className="text">Product</div>
                <div className="selector">
                    <div className="selector-child">{this.switchProduct()}</div>
                    {this.state.product ?
                        <button type="button" className="btn" onClick={()=>this.toggleProductState()}>Select</button> :
                        <button type="button" className="btn" onClick={()=>this.toggleProductState()}>New</button>}
                    {/*<button type="button" className="btn" onClick={()=>this.toggleProductState()}>New</button>*/}
                </div>
            </div>
        )
    }

    render() {

        return (
            <form onSubmit={(e)=>this.registerReportingTasks(e)} method="post" className="resister form">

                <div className="media-ids frame">
                    <div className="render-promotion-list">
                        <div className="search"></div>
                        <div className="list">

                            <table className="">
                                <thead className="">
                                <tr className="">
                                    <th className="">アカウント</th>
                                    <th className="">商品名</th>
                                    <th className="">メディア</th>
                                    <th className="">デバイス</th>

                                </tr>
                                </thead>

                                <tbody className="">
                                {this.renderPromotionlist()}
                                </tbody>
                            </table>

                        </div>
                    </div>

                    <div className="media-account-ids">


                        <div className="item selected-promotion">
                            <div className="">ターゲット</div>
                            <div className="selected">{this.state.selected_promotion.map((item, i)=><div
                                key={i}>{item}</div>)}</div>
                        </div>

                        <div className="item target">
                            <div className="">{this.renderPromotionSelector()}</div>
                        </div>

                        <div className="item account-id">
                            <div className="">Account id</div>
                            <div className=""><input onChange={(e)=>this.updateInput(e.target.value, 'account_id')}/>
                            </div>
                        </div>

                        <div className="item campaign-id">
                            <div className="">Campaign id</div>
                            <div className=""><input onChange={(e)=>this.updateInput(e.target.value, 'campaign_id')}/>
                            </div>
                        </div>

                        <div className="item register">
                            <input type="submit" className="" value='register'/>

                        </div>
                    </div>
                </div>
            </form>
        )

    }

}