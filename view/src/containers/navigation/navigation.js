/**
 * Created by YasumasaTakemura on 2017/03/30.
 */

import React, {Component} from 'react'
import {connect} from 'react-redux';
import {Link} from 'react-router';
import {navigation} from '../../components/navigation/navigation';
import '../../index.css'

// Navigation

let links = ['top','resister', 'report', 'tasks','table'];
let logout = ['logout'];

export default class Navigation extends Component {

    render() {
                return (
                <div style={{height:'50px'}}>
                    <div className="nav-bar" >
                        <div className="nav-list">{navigation(links)}</div>
                        <div style={{marginLeft:'20%',flex:1,width:'20%'}}> user </div>
                    </div>

                    {this.props.children}
                </div>

        )
    }
}

