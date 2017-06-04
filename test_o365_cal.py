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
# category_dict = {'[mtg]':'00:00:00Z','[work]':'00:00:00Z','[study]':'00:00:00Z','[fun]':'00:00:00Z','[move]':'00:00:00Z','[other]':'00:00:00Z'}

import time
import datetime

import re



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

    bookings = []
    category_dict = category_dict
    for cal in schedule.calendars:
        print('attempting to fetch events for',e)
        try:
            print('start is ', start)
            print('end is ', end)
            result = cal.getEvents(start=start,end=end, eventCount=100)
            print('Got events',result,'got',len(cal.events))
        except:
            print('failed to fetch events')

        print('attempting for event information')
        time_string_time = '%H:%M:%SZ'
        for event in cal.events:
            event = event.fullcalendarioJson()
            end_time = time.mktime(time.strptime(event['end'], '%Y-%m-%dT%H:%M:%SZ'))
            start_time = time.mktime(time.strptime(event['start'], '%Y-%m-%dT%H:%M:%SZ'))

            event_time = end_time - start_time
            event_time = time.strftime(time_string_time, time.gmtime(event_time))
            event.update({'event_time': event_time})

            bookings.append(event)

            for key in category_dict:
               title = event['title']
               if key in title:
                   n = category_dict[key]

                   event_time = str(event_time)[0:-1].split(':')
                   n = str(n)[0:-1].split(':')
                   event_time = int(event_time[0]) * 3600 + int(event_time[1]) * 60 + int(event_time[2])
                   n = int(n[0]) * 3600 + int(n[1]) * 60 + int(n[2])
                   n += event_time
                   n = time.strftime(time_string_time, time.gmtime(n))
                   category_dict[key] = n
                   #print(category_dict)
                   break

    # format json
    json_outs[e] = bookings
    json_outs[e] = category_dict

    events_all = json.dumps(bookings,sort_keys=True,indent=4)
    category_all = json.dumps(category_dict,sort_keys=True,indent=4)

    return(events_all, category_all)







#if __name__ == '__main__':
def get_date(start=None,end=None):

    # get time format
    time_string = '%Y-%m-%dT%H:%M:%SZ'

    if start == None:
      # get today start
      start = time.strftime(time_string)
      start = start[0:10] + 'T00:00:00Z'
      print('start is ',start)

    if end == None:
      # get today end
      end = time.time()
      end += 60*60*24
      end = time.gmtime(end)
      end = time.strftime(time_string,end)
      end = end[0:10] + 'T00:00:00Z'
      print('end is ',end)

    # get month start
    start_month = time.strftime(time_string)
    start_month = start_month[0:7] + '-01T00:00:00Z'
    print('start_month is ', start_month)

    # temp
    start = '2017-06-02T00:00:00Z'
    end = '2017-06-03T00:00:00Z'
    #start_month = '2017-06-01T00:00:00Z'

    return start,end,start_month


#if __name__ == '__main__':
def execution(start='YYYYMMDD',end='YYYYMMDD'):

    get_date_result = get_date()
    start_month = get_date_result[2]

    if start == 'YYYYMMDD':
      start = get_date_result[0]
      end = get_date_result[1]
    else:

#custom start is  20170602
#custom end is  20170601
#custom start formatted is  201-0-0T00:00:00Z
#custom end formatted is  201-0-0T00:00:00Z

      print('custom start is ', start)
      print('custom end is ', end)
      YYYY = start[0:4]
      MM = start[4:6]
      DD = start[6:8]
      start = YYYY + '-' + MM + '-' + DD + 'T00:00:00Z'
      YYYY = end[0:4]
      MM = end[4:6]
      DD = end[6:8]
      end = YYYY + '-' + MM + '-' + DD + 'T00:00:00Z'
      print('custom start formatted is ', start)
      print('custom end formatted is ', end)

    outputs = get_calender_format(start,end,category_dict)
    events_all = outputs[0]
    category_all = outputs[1]
    print(events_all)
    print(category_all)

    # reset dict
    for key in category_dict.keys():
      category_dict[key] = '00:00:00Z'
    print('category_dict is ', category_dict)


    outputs_month = get_calender_format(start_month,end,category_dict)
    events_all_month = outputs_month[0]
    category_all_month = outputs_month[1]
    print(events_all_month)
    print(category_all_month)

    return start,end,start_month,category_all,category_all_month
