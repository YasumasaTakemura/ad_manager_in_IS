/**
 * Created by YasumasaTakemura on 2017/03/30.
 */

import React, {Component} from 'react'
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';


export function navigation(links) {
    let hover = false
    return links.map((link, index)=> {
        return (
            <div key={index} className="nav-link">
                <Link style={{textDecoration: 'none'}} to={link}
                      key={index}> {link}</Link>
            </div>

        )}

    )

}



