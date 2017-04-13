/**
 * Created by YasumasaTakemura on 2017/03/31.
 */
import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import JsonTable from 'react-json-table';
import {Table, Thead, Th, Tr, Td} from 'reactable'
import SearchInput, {createFilter} from 'react-search-input'
import chunk from 'chunk'
import {Calender} from '../../components/calender/calender'
import {DataTable} from '../../components/report/datatable'
import {yenFormat, floatFormat, pointFormat, percentageFormat, strToDate, dateToStr} from '../../utils/funcs'
const array = require("array-extended");
import Select from 'react-select';
import 'react-select/dist/react-select.css';

function addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function compareDatetime(start, end, dataset) {

    if (start == undefined || end == undefined) {
        return
    }

    let datetime = []
    for (let data of dataset) {

        // dont know why but end will be shorten in a day
        if (start.getTime() <= data.getTime() && addDays(end, 1).getTime() >= data.getTime()) {
            datetime.push(data)
        }
    }

}

function filterDatetime(props) {

    let start = props.postParams.start_time
    let end = props.postParams.end_time
    let keys = ['date']
    let date_list = []
    let datetime_list = []

    let datasets = props.reportDataSets.data;

    // if dataset is filtered , replace with it
    if (props.filteredDatasets.data.length > 0) {
        datasets = props.filteredDatasets.data
    }

    for (let dataset of datasets) {
        for (let key in dataset) {
            if (key == 'date') {
                // console.log(datasets[key])
                date_list.push(dataset[key])
            }
        }
    }


    let uniqueDateList = date_list.filter(function (item, pos) {
        return date_list.indexOf(item) == pos;
    })


    for (let i in uniqueDateList) {
        datetime_list.push(new Date(Date.parse(uniqueDateList[i])))

    }

    let filteredDatetime = compareDatetime(start, end, datetime_list)

    //suspend further dev
    //because we can get data through from server

    // getFiltered(props, keys, uniqueDateList)
}

function searchUpdated(props, term) {
    props.pushInput({input: term})
    let keys = ['media_name', 'product_name', 'device']
    getFiltered(props, keys, term)
}

function getFiltered(props, keys, term) {
    let filteredItems = props.reportDataSets.data.filter(createFilter(term, keys))
    props.pushFilteredDatasets({data: filteredItems})
}

function pagination(dataset, len, pages) {
    return chunk(dataset, len)
}


function renderCalender(props) {
    return (
        <div className="calender">
            <div className="calender btn" onClick={()=>this.__onClick()}>Date</div>
            {this.props.toggler.calender ? <Calender/> : null}
        </div>

    )
}

function getDateRange(props) {
    let start_time
    let end_time
    let datasets = props.reportDataSets.data;

    // if dataset is filtered , replace with it
    if (props.filteredDatasets.data.length > 0) {
        datasets = props.filteredDatasets.data
    }

    let start = array.min(datasets, 'date')
    let end = array.max(datasets, 'date')


    for (let s in start) {
        if (s == 'date') {
            start_time = start[s]
        }
    }
    for (let e in end) {
        if (e == 'date') {
            end_time = end[e]
        }
    }

    return {start: strToDate(start_time), end: strToDate(end_time)}
}


function aggregateDatasets(props, keyName) {
    let sum = 0;
    let datasets = props.reportDataSets.data;

    // if dataset is filtered , replace with it
    if (props.filteredDatasets.data.length > 0) {
        datasets = props.filteredDatasets.data
    }

    for (let key of datasets) {
        sum += key[keyName]
    }

    return sum
}



export class ReportTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pageIndex: 0,
            selected: 'select'

        }
    }

    crud = new CRUD(this.props)


    componentWillMount() {
        let endpoint = 'get_report_by_product'
        this.crud.getRequest(this.props, endpoint)
    }

    renderPagenation(datasets) {
        return (
            <ul className="pagination">
                {this.state.pageIndex == 0 ? <li >Prev</li> :
                    <li onClick={()=>this.setState({pageIndex: this.state.pageIndex - 1})}>Prev</li>}


                {datasets.map((item, index)=><li key={index} onClick={()=>this.setState({pageIndex: index})}>{index + 1}</li>)}

                {this.state.pageIndex == datasets.length - 1 ? <li>Next</li> :
                    <li onClick={()=>this.setState({pageIndex: this.state.pageIndex + 1})}> Next</li>}
            </ul>
        )
    }

    __openCalender() {
        this.props.toggle({
            ...this.props.toggler,
            calender: true
        })
    }

    renderCalender() {
        return (
            <div className="toggle-calender">
                {this.props.toggler.calender ?
                    <button className="toggle-calender btn open">Date</button> :
                    <button className="toggle-calender btn closed" onClick={()=>this.__openCalender()}>Date</button>
                }

            </div>

        )
    }

    __getReport(props) {
        this.crud.getReportWithTimeRange(props)
        console.log('done')
    }

    __getStart_time() {
        var options = {year: "numeric", month: "numeric", day: "numeric", "weekday": "short"};
        return this.props.postParams.start_time.toLocaleString("ja-JP", options)
    }

    __getEtnd_time() {
        var options = {year: "numeric", month: "numeric", day: "numeric", "weekday": "short"};
        return this.props.postParams.end_time.toLocaleString("ja-JP", options)
    }

    selectTypesOfGroup(endpoint,label) {
        this.crud.getRequest(this.props, endpoint)
        this.props.pushSelected({selected: label})

    }


    __valueRenderer(v) {

        if (v !== undefined) {
            this.props.pushSelected({selected: v.label})

        }
    }

    __runTaskManager() {
        this.crud.runTaskManager(this.props)

    }

    __renderDropDown() {

        var options = [
            {value: 'get_report_by_media', label: 'by_media', clearableValue: false},
            {value: 'get_report_by_product', label: 'by_product'},
            {value: 'get_daily_report_by_promotion', label: 'by_promotion'},
            // {value: 'by_account', label: 'by_account'},
            // {value: 'by_product', label: 'by_product'},
            // {value: 'by_creatives', label: 'by_creative'},
            // {value: 'all', label: 'all'},
        ];


        return <Select
            clearable={false}
            name="form-field-name"
            options={options}
            onChange={(v,l)=>this.selectTypesOfGroup(v,l)}
            value={this.props.selected.selected}
        />
    }


    render() {

        filterDatetime(this.props)

        // set variable from redux which is data and header
        let dataset = this.props.reportDataSets.data
        let header = this.props.reportDataSets.header

        // if dataset is filtered , replace with it
        if (this.props.filteredDatasets.data.length > 0) {
            dataset = this.props.filteredDatasets.data
        }

        //get paged datasets with chunk list
        let datasets = pagination(dataset, 10)

        //set start and end value
        let start, end;

        if (datasets[0] !== undefined && datasets[0].date === undefined) {
            start = strToDate(this.props.postParams.start_time)
            end = strToDate(this.props.postParams.end_time)

        } else {
            start = getDateRange(this.props).start
            end = getDateRange(this.props).end
        }

        ////////////////////////////////
        //KPIs
        ////////////////////////////////

        // variables for aggregated KPIs
        let spend = aggregateDatasets(this.props, 'spend')
        let imps = aggregateDatasets(this.props, 'impressions')
        let clicks = aggregateDatasets(this.props, 'clicks')
        let cvs = aggregateDatasets(this.props, 'cvs')
        let cpa = yenFormat(floatFormat(spend / cvs, 1))
        // let ctr = floatFormat(clicks / imps, 5) * 100
        let ctr = ((clicks / imps) * 100).toFixed(2)
        let cvr = ((cvs / clicks) * 100).toFixed(2)

        spend = yenFormat(spend)
        imps = pointFormat(imps)
        clicks = pointFormat(clicks)
        cvs = pointFormat(cvs)

        return (
            <div className="data-table">

                <div className="aggregate-report">

                    <div className="ag-child">
                        <div className="ag-date">
                            <div className="kpi-text">Date</div>
                            <div className="star_time">{start}</div>
                            <div className="end_time">{end}</div>
                        </div>
                    </div>
                    <div className="ag-spend">
                        <div className="kpi-text">Spend</div>
                        <div className="kpi-number">{spend}</div>
                    </div>

                    <div className="ag-impressions">
                        <div className="kpi-text">imp</div>
                        <div className="kpi-number">{imps}</div>
                    </div>

                    <div className="ag-clicks">
                        <div className="kpi-text">click</div>
                        <div className="kpi-number">{clicks}</div>
                    </div>
                    <div className="ag-cvs">
                        <div className="kpi-text">cvs</div>
                        <div className="kpi-number">{cvs}</div>
                    </div>
                    <div className="ag-cpa">
                        <div className="kpi-text">CPA</div>
                        <div className="kpi-number">{cpa}</div>
                    </div>
                    <div className="ag-ctr">
                        <div className="kpi-text">CTR</div>
                        <div className="kpi-number">{ctr}%</div>
                    </div>
                    <div className="ag-cvr">
                        <div className="kpi-text">CVR</div>
                        <div className="kpi-number">{cvr}%</div>
                    </div>
                </div>


                <div className="tools">

                    <div className="left-side">
                        <div className="submit">
                            <div className="btn" onClick={()=>this.__getReport(this.props)}>
                                <div>Update</div>
                            </div>
                        </div>
                        <div className="btn">
                            <div className="export">Export</div>
                        </div>
                        <div className="btn">
                            <div onClick={()=>this.__runTaskManager()}>Run Tasks</div>
                        </div>
                        <div className="btn">Graph</div>
                        <div className="btn">Templates</div>
                        <div className="btn">Edit</div>
                    </div>

                    <div className="right-side">

                        <div className="date">
                            <div className="date-child">
                                <div className="btn">{this.renderCalender()}</div>
                                <div className="date start_time">{this.__getStart_time()}</div>
                                <div> -</div>
                                <div className="date end_time">{this.__getEtnd_time()}</div>
                            </div>

                        </div>

                        <div className="calender">
                            {this.props.toggler.calender ? <Calender {...this.props}/> : null}
                        </div>


                        <div className="dropdown">
                            {this.__renderDropDown()}
                        </div>

                        <SearchInput className="search-input" onChange={(e)=>searchUpdated(this.props, e)}/>
                    </div>
                </div>

                <DataTable header={header} rows={datasets[this.state.pageIndex]} {...this.props}/>

                {/*<JsonTable*/}
                    {/*rows={datasets[this.state.pageIndex]}*/}
                    {/*columns={header}/>*/}
                <div>
                    {this.renderPagenation(datasets)
                    }
                </div>
            </div>
        )
    }
}

