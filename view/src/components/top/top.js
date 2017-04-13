/**
 * Created by YasumasaTakemura on 2017/03/31.
 */

import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import axios from 'axios'

export class TopPage extends Component{

    render(){
        return <div style={{backgroundColor:'gray'}}>
            <div style={{font:'white'}}> color </div>
            <div style={{font:'white'}}> color </div>
            <div style={{font:'white'}}> color </div>
            <div style={{font:'white'}}> color </div>
            <div style={{font:'white'}}> color </div>
        </div>
    }
}