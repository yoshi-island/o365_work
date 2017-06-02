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
#category_dict = {'[mtg]':0,'[work]':0,'[study]':0,'[fun]':0,'[move]':0,'[other]':0}

import time
from datetime import datetime

import re



if __name__ == '__main__':
    #veh = open('./pw/veh.pw','r').read()
    #vj = json.loads(veh)

    schedules = []
    json_outs = {}

    #for veh in vj:
        #e = veh['email']
    e = user
        #p = veh['password']
    p = password


    # get time format
    time_string = '%Y-%m-%dT%H:%M:%SZ'

    start = time.time()
    start = time.strftime(time_string)
    print('now is ', start)
    start = start[0:10] + 'T00:00:00Z'
    print('start is ',start)

    end = time.time()
    end += 60*60*24*1.5
    end = time.gmtime(end)
    end = time.strftime(time_string,end)
    print('end time is ', end)
    end = end[0:10] + 'T00:00:00Z'
    print('end is ',end)



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
            #result = cal.getEvents()
            result = cal.getEvents(start=start,end=end, eventCount=100)
            print('Got events',result,'got',len(cal.events))
        except:
            print('failed to fetch events')

        print('attempting for event information')
        time_string_time = '%H:%M:%SZ'
        for event in cal.events:
            #print('HERE!')
            event = event.fullcalendarioJson()
            end_time = time.mktime(time.strptime(event['end'], '%Y-%m-%dT%H:%M:%SZ'))
            start_time = time.mktime(time.strptime(event['start'], '%Y-%m-%dT%H:%M:%SZ'))
            event_time = end_time - start_time
            event_time = time.strftime(time_string_time, time.gmtime(event_time))
            print('event time is ', event_time)
            event.update({'event_time': event_time})

            bookings.append(event)
            print('bookings is ', bookings)


        for key in category_dict:
            print('key is ', key)
            print('key type is ', type(key))
            title = event['title'].encode('utf-8')
            print('title type is ', type(title))
            print('title is ', title)
            result = re.search(r'[work]', title)
            print('result is ',result)
 
            if result is not None:
                n = category_dict['[work]']
                n += 1
                category_dict['[work]'] = n
                #break

        print('category_dict is ',category_dict)



    print('bookings is ', bookings)
    json_outs[e] = bookings

    events_all = json.dumps(bookings,sort_keys=True,indent=4)
    print(events_all)

    #with open('bookings.json','w') as outs:
    #    outs.write(json.dumps(json_outs,sort_keys=True,indent=4))
    
    
#To the King!
