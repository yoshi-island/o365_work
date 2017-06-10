# python

from O365 import *
import json

# temp: to avoid ssl error
import urllib3
urllib3.disable_warnings()

import password_list
user = password_list.user
password = password_list.password
category_dict = password_list.category_dict
# category_dict = {'[mtg]':'','[work]':'','[study]':'','[fun]':'','[move]':'','[other]':''}

import time
import datetime
import re #find
import math


def get_date(start=None,end=None):

    # get time format
    time_string = '%Y-%m-%dT%H:%M:%SZ'

    # get today start time
    if start == None:
      start = time.strftime(time_string)
      start = start[0:10] + 'T00:00:00Z'

    # get today end time
    if end == None:
      end = time.strftime(time_string)
      end = end[0:10] + 'T23:59:59Z'

    # get month start time
    start_month = time.strftime(time_string)
    start_month = start_month[0:7] + '-01T00:00:00Z'

    return start,end,start_month


def get_calender_format(start=None, end=None, category_dict=None):

    if (start or end) == None:
      print('start or end is not defined')
      exit()

    if (category_dict) == None:
      print('category_dict is not defined')
      exit()

    schedules = []
    json_outs = {}

    e = user
    p = password

    schedule = Schedule((e,p))

    try:
        result = schedule.getCalendars()
        print('Fetched calendars for',e,'was successful:',result)
    except:
        print('Login failed for',e)


    # format category_dict
    category_dict = category_dict
    for key in category_dict.keys():
      category_dict[key] = 0

    bookings = []
    for cal in schedule.calendars:
        print('attempting to fetch events for',e)
        try:
            result = cal.getEvents(start=start,end=end, eventCount=100000) #fixme:eventcount want get all events
            print('Got events',result,'got',len(cal.events))
        except:
            print('failed to fetch events')

        print('attempting for event information')
        time_string_time = '%H:%M:%SZ' #fixme: event cannot be over a day
        time_string_time_sum = '%dT%H:%M:%SZ' #fixme: time sum cannot be over a month
        for event in cal.events:
            event = event.fullcalendarioJson()

            # append event time info
            end_time = time.mktime(time.strptime(event['end'], '%Y-%m-%dT%H:%M:%SZ'))
            start_time = time.mktime(time.strptime(event['start'], '%Y-%m-%dT%H:%M:%SZ'))
            event_time = end_time - start_time
            event_time = time.strftime(time_string_time, time.gmtime(event_time))
            event.update({'event_time': event_time})
            bookings.append(event)

            # update category dict
            for key in category_dict:
               title = event['title']
               if key in title:
                   n = category_dict[key]
                   # format
                   if ':' in str(event_time):
                       event_time = str(event_time)[0:-1].split(':')
                       event_time = int(event_time[0]) * 3600 + int(event_time[1]) * 60 + int(event_time[2])
                   n += event_time
                   category_dict[key] = n

    # format category_dict
    for key in category_dict.keys():
      category_sec = category_dict[key]
      category_hour = int(category_sec/60/60)
      category_min = int(category_sec/60%60)
      category_dict[key] = str(category_hour) + ':' + str(category_min)

    # format json
    events_all = json.dumps(bookings,sort_keys=True,indent=4, ensure_ascii=False)
    #print('events_all is ', events_all)

    category_all = json.dumps(category_dict,sort_keys=True,indent=4, ensure_ascii=False)
    #print('category_all is ', category_all)

    return(events_all, category_all)




#if __name__ == '__main__':
#    start = 'YYYYMMDD'
#    end = 'YYYYMMDD'
def execution(start='YYYYMMDD',end='YYYYMMDD'):

    get_date_result = get_date()
    get_date_result = ('2017-06-08T00:00:00Z', '2017-06-09T23:59:59Z', '2017-06-01T00:00:00Z')

    # set date time info
    start_month = get_date_result[2]
    if start == 'YYYYMMDD': # fixme: judged by only looking up start
      start = get_date_result[0]
      end = get_date_result[1]
    else:
      YYYY = start[0:4]
      MM = start[4:6]
      DD = start[6:8]
      start = YYYY + '-' + MM + '-' + DD + 'T00:00:00Z'
      YYYY = end[0:4]
      MM = end[4:6]
      DD = end[6:8]
      end = YYYY + '-' + MM + '-' + DD + 'T23:59:59Z'

    # get todays work
    print('start is', start)
    print('end is', end)
    outputs = get_calender_format(start,end,category_dict)
    events_all = outputs[0]
    category_all = outputs[1]
    #print(events_all)
    print(category_all)

    # reset dict
    for key in category_dict.keys():
      category_dict[key] = ''

    # get monthly work
    print('start_month is', start_month)
    print('end is', end)
    outputs_month = get_calender_format(start_month,end,category_dict)
    events_all_month = outputs_month[0]
    category_all_month = outputs_month[1]
    #print(events_all_month)
    print(category_all_month)

    return start,end,start_month,category_all,category_all_month
