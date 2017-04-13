import React, {Component, PropTypes} from 'react';
import ReactDOM from 'react-dom';
// import {Router, Route} from 'react-router';
import createHistory from 'history/createBrowserHistory'
import {BrowserRouter as Router, Route, Link, Switch} from 'react-router-dom'
import {Provider} from 'react-redux'
import {createStore, compose, combineReducers} from 'redux'


const history = createHistory()

//////////////////////////////
// reducer
//////////////////////////////
import {
    Report,
    Input,
    FilteredDatasets,
    post,
    toggle,
    kpis,
    selected,
    initializedResisterAccount,
    selectedItems,
    promotionList,
} from './store/reducer/reducer'


//////////////////////////////
// auth
//////////////////////////////
import {Auth, AuthenticatedUser, Guest} from './containers/auth'

//////////////////////////////
// store
//////////////////////////////
import {_ReportTable, _ToggleManager,_RegisterPage} from './store/connects'


//////////////////////////////
// nav
//////////////////////////////
import  Navigation from './containers/navigation/navigation'


//////////////////////////////
//login management
//////////////////////////////
import {Login} from './store/connects'
import {_TopPage} from './store/connects'
import {_PromotionList} from './store/connects'


//////////////////////////////
// render
//////////////////////////////
import renderFormsForTest from './containers/report/report'


//////////////////////////////
//combine reducer
//////////////////////////////
const reducers = combineReducers({
    Report,
    Input,
    FilteredDatasets,
    post,
    toggle,
    kpis,
    selected,
    initializedResisterAccount,
    selectedItems,
    promotionList,
});

export let store = createStore(reducers,
    compose(window.devToolsExtension && window.devToolsExtension()));

//router
ReactDOM.render(
    <Provider store={store}>

        <Router history={history}>

            <Navigation>
                <Route exact path='/top' component={_PromotionList}/>
                {/*<Route path='/top' component={_PromotionList}/>*/}
                {/*<Route path='/table' component={_MyTable}/>*/}
                <Route exact path='/report' component={_ReportTable}/>
                <Route exact path='/resister' component={_RegisterPage}/>


            </Navigation>


        </Router>
    </Provider >
    ,
    document.getElementById('root')
);
