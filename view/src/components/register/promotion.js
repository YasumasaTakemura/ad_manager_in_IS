/**
 * Created by YasumasaTakemura on 2017/04/05.
 */

import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import {yenFormat, floatFormat, pointFormat, percentageFormat, strToDate, dateToStr, isEmpty} from '../../utils/funcs'
import Select from 'react-select';
import '../../index.css'


export class PromotionRender extends Component {

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
    // Account
    ////////////////////////////////////////

    renderAccountInput() {
        return <input onChange={(e)=>this.props.setAccount({name: e.target.value, id: 0})}
                      className="selector-child" name="account"/>
    }

    toggleAccountState() {
        this.setState({account: !this.state.account})

    }

    switchAccount(key) {
        return this.state.account ? this.renderAccountInput() : this.renderAccountSelector();

    }

    selectAccount(v, l) {

        this.props.selectAccount({
            name: l[0].label,
            id: l[0].value,
        })


        this.props.setAccount({
            name: l[0].label,
            id: parseInt(l[0].value)
        })


    }

    renderAccountSelector() {
        let __temp = []
        let datasets = this.props.initializedResisterAccount
        if (!isEmpty(datasets)) {
            for (let account of datasets.accounts) {
                for (let key in account) {
                    if (key == 'account_name') {
                        __temp.push({value: account.id, label: account[key], clearableValue: false})

                    }
                }
            }
        }

        return (
            <Select
                clearable={false}
                name={'account'}
                value={this.props.postParams.selected.account.name}
                options={__temp}
                onChange={(v, vl)=>this.selectAccount(v, vl)}
            />
        )
    }

    renderAccount() {

        return (
            <div className="account">
                <div className="text">Account</div>
                <div className="selector">
                    <div className="selector-child">{this.switchAccount()}</div>
                    {this.state.account ?
                        <button type="button" className="btn" onClick={()=>this.toggleAccountState()}>Select</button> :
                        <button type="button" className="btn" onClick={()=>this.toggleAccountState()}>New</button>}
                </div>
            </div>
        )
    }

    ////////////////////////////////////////
    // Product
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

    renderProductSelector() {
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


    ////////////////////////////////////////
    // device
    ////////////////////////////////////////

    selectDevice(v, l) {

        this.props.setDevice({
            name: l[0].label,
            id: parseInt(l[0].value)
        })

    }

    renderDeviceSelector() {
        let __temp = []
        let datasets = this.props.initializedResisterAccount
        if (!isEmpty(datasets)) {

            for (let device of datasets.device) {
                for (let key in device) {
                    if (key == 'device') {
                        __temp.push({value: device.id, label: device[key]})

                    }
                }
            }

        }

        return (
            <Select
                clearable={false}
                name={'device'}
                value={this.props.postParams.selected.device.name}
                options={__temp}
                onChange={(v, vl)=>this.selectDevice(v, vl)}
            />
        )
    }

    renderDevice() {
        return (
            <div className="divece">
                <div className="text">Device</div>
                <div
                    className="selector">{this.renderDeviceSelector()}</div>
            </div>
        )
    }

    ////////////////////////////////////////
    // media
    ////////////////////////////////////////
    selectMedia(v, l) {
        console.log('>>>>>>>>>>>>>>.')
        this.props.setMedia({
            name: l[0].label,
            id: parseInt(l[0].value)
        })

    }

    renderMediaSelector() {
        let __temp = []
        let datasets = this.props.initializedResisterAccount
        if (!isEmpty(datasets)) {

            for (let media of datasets.medias) {
                for (let key in media) {
                    if (key == 'media_name') {
                        __temp.push({value: media.id, label: media[key]})

                    }
                }
            }
        }
        return (
            <Select
                clearable={false}
                name={'media'}
                value={this.props.postParams.selected.media.name}
                options={__temp}
                onChange={(v, vl)=>this.selectMedia(v, vl)}
            />
        )
    }

    renderMedia() {
        return (
            <div className="media">
                <div className="text">Media</div>
                <div
                    className="selector">{this.renderMediaSelector()}</div>
            </div>
        )
    }


    ////////////////////////////////////////
    // resister promotion
    ////////////////////////////////////////
    resisterPromotion(e) {
        e.preventDefault()
        let crud = new CRUD(this.props)
        let res = crud.resisterPromotion()
        console.log(res)
        if (res) alert('new promotion have just registered!')

    }


    render() {

        // if the order of renderMedia and renderDevice is oposite , renderMedia is not gonna work
        return (
            <form onSubmit={(e)=>this.resisterPromotion(e)} method="post" className="resister form">
                <div className="item">{this.renderAccount()}</div>
                <div className="item">{this.renderProduct()}</div>
                <div className="item">{this.renderMedia()}</div>
                <div className="item">{this.renderDevice()}</div>

                <div className="submit">
                    <button type="submit" className="submit-btn">Register</button>
                </div>
            </form>
        )
    }

}