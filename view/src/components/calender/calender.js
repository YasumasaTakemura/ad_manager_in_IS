/**
 * Created by YasumasaTakemura on 2017/04/02.
 */
import React, {Component, PropTypes} from 'react';
import {CRUD} from '../../utils/funcs'
import InfiniteCalendar, {withRange, Calendar}from 'react-infinite-calendar';
import 'react-infinite-calendar/styles.css';
const enhanceWithClickOutside = require('react-click-outside');


// Render the Calendar
var today = new Date();
var yesterday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1);
var lastWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
var lastYear = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());

class _Calender extends Component {
    themeColor = {
        accentColor: '#435052',
        floatingNav: {
            // background: 'rgba(56, 87, 138, 0.94)',
            background: '#435052',
            chevron: '#FFFFFF',
            color: '#FFF',
        },
        headerColor: '#435052',
        selectionColor: '#435052',
        textColor: {
            active: '#FFF',
            default: '#333',
        },
        todayColor: '#FF00F0',
        weekdayColor: '#559FFF',
    };

    locale = {
        headerFormat: 'YYY, MM , DD D',
    }

    __onSelect(date) {

        // event type  3  is for range
        if (date.eventType == 3) {
            this.props.post({
                    start_time: date.start,
                    end_time: date.end,
            })
        }
    }

    handleClickOutside() {
        this.props.toggle({
            ...this.props.toggler,
            calender: false
        })
    }

    render() {

        let selected;
        if (this.props.postParams.start_time !== undefined) {
            let date = this.props.postParams;
            console.log(date)
            selected = {
                 start: date.start_time,
                end: date.end_time,
            }
        }else {
            selected = {
                start: yesterday,
                end: today
            }
        }


        return (
            <InfiniteCalendar
                className="infinite-calendar"
                theme={this.themeColor}
                locale={this.locale}
                width={400}
                height={300}

                disabledDays={[0, 90]}
                min={new Date(2016, 0, 1)}
                minDate={lastYear}
                maxDate={today}
                onSelect={(d)=>this.__onSelect(d)}
                Component={withRange(Calendar)}
                selected={selected}
            />
        )
    }
}

// to enhance the class to implement click-outside function
export let Calender = enhanceWithClickOutside(_Calender)