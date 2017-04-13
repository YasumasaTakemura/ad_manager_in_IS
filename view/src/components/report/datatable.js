/**
 * Created by YasumasaTakemura on 2017/04/11.
 */
import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import JsonTable from 'react-json-table';
import {Table, Thead, Th, Tr, Td} from 'reactable'
import SearchInput, {createFilter} from 'react-search-input'
import chunk from 'chunk'
import {Calender} from '../../components/calender/calender'
import {isEmpty} from '../../utils/funcs'
const array = require("array-extended");
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import '../../index.css'

export class DataTable extends Component {

    renderHeader(header) {
        return <tr>
            {header.map((item)=><th>{item}</th>)}
        </tr>

    }

    renderColmuns(dataset, header) {
        console.log(dataset)
        let row = []

        for (let key in dataset) {
            for (let head of header) {
                if (key == head) {

                    row.push(<td className=''>{dataset[key]}</td>)
                }
            }
        }

        return row


    }

    renderRows(datasets, header, type) {

        // empty validation
        if (!isEmpty(datasets) || !isEmpty(header)) {

            // return rows by types of by_*****
            switch (type) {

                case type = 'by_promotion':
                    return datasets.map((dataset)=> {

                            return <tr>
                                <td className="">{dataset.promotion_id}</td>
                                <td className="">{dataset.date}</td>
                                <td className="">{dataset.media_name}</td>
                                <td className="">{dataset.device}</td>

                                <td className="">{dataset.product_name}</td>
                                <td className="">{dataset.spend}</td>
                                <td className="">{dataset.impressions}</td>
                                <td className="">{dataset.clicks}</td>
                                <td className="">{dataset.cvs}</td>
                                <td className="">¥{(dataset.spend / dataset.cvs).toFixed(0)}</td>
                                <td className="">{(dataset.clicks / dataset.impressions * 100).toFixed(2)}%</td>
                                <td className="">{(dataset.cvr * 100).toFixed(1)}%</td>
                                {/*<td className="">{(dataset.cvs / dataset.clicks * 100).toFixed(1)}%</td>*/}

                            </tr>
                        }
                    )

                case type = 'by_media':
                    return datasets.map((dataset)=> {

                        return <tr>
                            <td className="">{dataset.media_name}</td>
                            <td className="">{dataset.product_name}</td>
                            <td className="">{dataset.device}</td>
                            <td className="">{dataset.spend}</td>
                            <td className="">{dataset.impressions}</td>
                            <td className="">{dataset.clicks}</td>
                            <td className="">{dataset.cvs}</td>
                            <td className="">¥{(dataset.spend / dataset.cvs).toFixed(0)}</td>
                            <td className="">{(dataset.clicks / dataset.impressions * 100).toFixed(2)}%</td>
                            <td className="">{(dataset.cvs / dataset.clicks * 100).toFixed(1)}%</td>
                        </tr>
                    })

                // by_product
                default:
                    return datasets.map((dataset)=> {

                        return <tr>
                            <td className="">{dataset.product_name}</td>
                            <td className="">{dataset.spend}</td>
                            <td className="">{dataset.impressions}</td>
                            <td className="">{dataset.clicks}</td>
                            <td className="">{dataset.cvs}</td>
                            <td className="">¥{(dataset.spend / dataset.cvs).toFixed(0)}</td>
                            <td className="">{(dataset.clicks / dataset.impressions * 100).toFixed(2)}%</td>
                            <td className="">{(dataset.cvr * 100).toFixed(1)}%</td>
                            {/*<td className="">{(dataset.cvs / dataset.clicks * 100).toFixed(1)}%</td>*/}

                        </tr>
                    })
            }
        }
    }

    render() {

        const {selected,rows,header} = this.props;

        // to exclude 'fee' element, slice
        let headers = header.slice(1,)
        let type = selected.selected[0].label

        return (
            <table className="data-table">

                <thead>
                {this.renderHeader(headers)}
                </thead>

                <tbody>
                {this.renderRows(rows, headers, type)}
                </tbody>


            </table>
        )

    }
}