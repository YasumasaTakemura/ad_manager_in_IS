/**
 * Created by YasumasaTakemura on 2017/03/31.
 */
import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import axios from 'axios'

let base = 'http://0.0.0.0:8080/';
let login = base + 'loggin';


function combineUrl(base,endpoints){
    return base + endpoints
}

function setTokenOnHeaders(token) {
    if(token){
        axios.defaults.headers.common['Authorization'] = 'Bearer '+ token
        axios.defaults.headers.common['Access-Control-Allow-Origin'] = '/*'
    }else{
        //delete axios.defaults.headers.common['Authorization']
    }
}

function validateToken(endpoint) {


        //get token from local storage
        let token = localStorage.getItem('token')

        //set Authorization on navigation as default
        setTokenOnHeaders(token)


        //post token to authorize
        axios.post(endpoint, token).then((res)=> {
                console.log('auth??')
                console.log(token)

                if (res.data.res.token === token) {
                    console.log('you are authorized')
                    console.log(res.data.res)
                    this.props.PushCurrentUser({username: res.data.res.username, userID: res.data.res.userID, auth: true})
                }

            }
        )
    }



export class Auth extends Component {

    componentWillMount() {
        combineUrl(base,login)
        console.log('auth??')
        validateToken();

    }

    componentWillUpdate(nextProps) {
        //if you want to validate user login status
        //activate the method below

        //*-- --*//
        //this.ValidateToken()
    }



    render() {
        console.log(this.props._temp.test.loading)
        if(this.props._temp.test.loading) return <div style={this.props._temp.test.loading?{margin:'0 auto', zIndex:100000,opacity:'0.5',backgroundColor:'gray', width:'100vw' , height:'100vh'}:null}>Loading ...</div>
        return (
            <div>
                {this.props.children}
            </div>
        )
    }
}

export class AuthenticatedUser extends Component {
    componentWillMount() {
        console.log('IsAuthenticated true')
        console.log(this.props.CurrentUser.auth)
        this.validateUser()
    }


    validateUser() {
        if (!this.props.CurrentUser.auth) {
            console.log('IsAuthenticated true')
            console.log(this.props.CurrentUser)

            //dont know why but loading first time,  CurrentUser is null
            this.props.router.replace('/report')
        } else {
            this.props.router.replace('/login')
        }
    }


    render() {
        return (
            <div>
                {this.props.children}
            </div>
        )
    }

}

export class Guest extends Component {
    componentWillMount() {
        this.validateUser()
    }

    componentWillUpdate(nextProps) {
        //this.redirect()

    }

    validateUser() {
        if (this.props.CurrentUser.auth) {
            console.log('IsAuthenticated false')
            this.props.router.replace('/report')
        } else {
            this.props.router.replace('/')
        }
    }


    render() {
        return (
            <div>
                {this.props.children}
            </div>
        )
    }
}
