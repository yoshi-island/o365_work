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



def get_calender_format(start=None, end=None):

    if (start or end) == None:
      print('start or end is not defined')
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
    for cal in schedule.calendars:
        print('attempting to fetch events for',e)
        try:
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
                   break

    # format json
    json_outs[e] = bookings
    json_outs[e] = category_dict

    events_all = json.dumps(bookings,sort_keys=True,indent=4)
    category_all = json.dumps(category_dict,sort_keys=True,indent=4)

    return(events_all, category_all)







if __name__ == '__main__':

    # get time format
    time_string = '%Y-%m-%dT%H:%M:%SZ'

    start = time.time()
    start = time.strftime(time_string)
    start = start[0:10] + 'T00:00:00Z'
    print('start is ',start)

    end = time.time()
    end += 60*60*24*1.5
    end = time.gmtime(end)
    end = time.strftime(time_string,end)
    end = end[0:10] + 'T00:00:00Z'
    print('end is ',end)

    # temp
    start = '2017-06-02T00:00:00Z'
    end = '2017-06-04T00:00:00Z'

    outputs = get_calender_format(start,end)
    events_all = outputs[0]
    category_all = outputs[1]
    print(events_all)
    print(category_all)

    
