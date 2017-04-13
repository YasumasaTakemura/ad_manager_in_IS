/**
 * Created by YasumasaTakemura on 2017/04/02.
 */
import React, {Component, PropTypes} from 'react';
import * as action from '../../store/actions/actions'
import * as reducer from '../../store/reducer/reducer'

export default class ToggleManager extends Component {

    __onClick() {
        let toggle = this.props.toggler;
        let temp={}

        for(let t in toggle){
            if (toggle.hasOwnProperty(t)) {
                temp[t] = !toggle[t]
            }

        }
        console.log(temp)
        this.props.toggle(temp)

    }

    render() {
        return (
            <div style={{backgroundColor:'lightgray'}} onClick={()=>this.__onClick()}>
                {this.props.children}
            </div>
        )
    }
}