# -*- coding: utf-8 -*-
"""
Created on Sun May  3 11:34:52 2020

@author: sferg
"""

"""
Created on Thu Apr 30 12:04:19 2020

Author: Spencer Ferguson-Dryden
https://github.com/sfergusond

Implmentation of comment/description only upload

Uses: webbot from https://github.com/nateshmbhat/webbot
"""
import csv # won't need this when deployed
from webbot_exe import Browser
import webbot_exe
import StravaHelper
import R2WImporter
import datetime
import time

def main(r2w_data, web, a, b, policy, variance):        
    
    for r in r2w_data:
        r['distance'] = round(float(r['distance']) * 1609.34, 1)
        r['date'] = format_date(r['date'], '/', 'MDY')
        r['date'] = (r['date'][0], r['date'][1], r['date'][2])
    
    keep = ['date', 'distance', 'id']
    
    web = R2WImporter.login_strava(web) # LOGIN TO STRAVA
    
    # INITIALIZE CLIENT AND AUTHENTICATION
    CLIENT = StravaHelper.initialize_client(web = web, scope = 'activity:read_all')
    print('Authorized!\n')
    strava_data = StravaHelper.activities(a, b, client = CLIENT, keep = keep)
    
    strava_by_date = organize_by_date(strava_data)
    
    add_desc(r2w_data, strava_by_date, policy, variance, web) # [id, distance, desc]
    print('Success! Program will now quit.')
    
    return 
    
def upload(activities, web):
    count = 0
    for a in activities:
        t1 = time.time()
        
        url = 'https://www.strava.com/activities/' + str(a[0]) + '/edit'
        web.go_to(url)
        web.type('\n\n' + a[2], clear=False, id='activity_description')
        web.click(xpath='/html/body/div[3]/div/div/div/button')
        
        count += 1
        progress = 'Updating descriptions...'
        t2 = time.time()
        printProgressBar(count, len(activities), prefix = progress, length = 120, t1 = t1, t2 = t2)
    
    web.driver.close()
    
def add_desc(r2w, strava, policy, variance, web):
    result = []
    tmp = strava
    count = 0
    for r in r2w:
        t1 = time.time()
        if strava.get(r['date']) != None: #r['date'] in list(strava.keys()):
            index = match(r['distance'], tmp[r['date']], variance)
            if index != -1: # if a match exists, add
                
                if len(tmp[r['date']][index]) == 2: # desc already appended
                    tmp[r['date']][index].append(r['description'])
                else: # no desc exists
                    tmp[r['date']][index][2] += ('\n' + r['description'])
                    
                result.append(tmp[r['date']][index])
            else: # No viable match found, use given policy to handle
                if policy == 'create': # upload new
                    r['date'] = upload_date(r['date'])
                    r['distance'] = upload_distance(r['distance'])
                    R2WImporter.add_strava_entry(r, web)
                elif policy == 'ignore': # skip activity
                    continue
                else: # add to existing activity
                    if len(tmp[r['date']][0]) == 2: # desc already appended
                        tmp[r['date']][0].append(r['description'])
                    else: # no desc exists
                        tmp[r['date']][0][2] += ('\n' + r['description'])
                    result.append(tmp[r['date']][0])
        else: # No acitvity exists for the current day in the R2W dataset
            r['date'] = upload_date(r['date'])
            r['distance'] = upload_distance(r['distance'])
            R2WImporter.add_strava_entry(r, web)
            
        count += 1
        progress = 'Adding new activities...'
        t2 = time.time()
        printProgressBar(count, len(r2w), prefix = progress, length = 120, t1 = t1, t2 = t2)

    upload(result, web)
    
# Returns the index of the matched run in strava
# +/- 500 meters should be appropriate
def match(distance, strava, variance):
    for i in range(len(strava)):
        if strava[i][1] <= distance + 500 and strava[i][1] >= distance - 500:
            return i
    return -1

def organize_by_date(activities):
    master = {}
    count = 0
    
    for a in activities:
        date = format_date(a['date'])
        date = (date[0], date[1], date[2])

        if master.get(date) == None: #if date not in list(master.keys()):
            master[date] = [[a['id'], a['distance']]]
        else:
            master[date].append([a['id'], a['distance']])
        
        count += 1
        progress = 'Formatting activities...'
        printProgressBar(count, len(activities), prefix = progress, length = 100)
        
    return master

def format_date(date, sep = '-', order = 'YMD'):
    date = date.split(sep)
    
    if str.upper(order) == 'YMD':
        for i in range(3):
            date[i] = int(date[i])
        return date
    elif str.upper(order) == 'DMY':
        tmp = [int(date[2]), int(date[1]), int(date[0])]
        return tmp
    elif str.upper(order) == 'MDY':
        tmp = [int(date[2]), int(date[0]), int(date[1])]
        return tmp
    
def upload_date(date):
    result = f'{date[1]}/{date[2]}/{date[0]}'
    return result       
        
def upload_distance(distance):
    result = str(round(float(distance) * 0.000621371, 2))
    return result

def read_csv(a, b): # only needed locally
    li = []
    
    a = format_date(a)
    b = format_date(b)    
    a = datetime.datetime(a[0], a[1], a[2])
    b = datetime.datetime(b[0], b[1], b[2]) - datetime.timedelta(days=1) # align inclusivity between strava and r2w
    
    # Open csv and extract info into a list of dicts
    with open('activities.csv', 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            date = format_date(row['date'], '/', 'MDY')
            date = datetime.datetime(date[0], date[1], date[2])
            if date >= a and date <= b :
                li.append({'date': row['date'], 'distance': round(float(row['distance']),2), 'description': row['description'], 'time': row['time'], 'title': row['title'], 'type': row['type'], 'difficulty': row['difficulty'], 'avg_hr': row['avg_hr'], 'max_hr': row['max_hr']})
            
    return li
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '\r', t1 = None, t2 = None, step = 1):
    """
    Borrowed from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    if t1 != None and t2 != None:
        if iteration < total:
            remaining = (t2-t1)*((total/step) - (iteration/step))
        else: remaining = 0
        est_time = str(datetime.timedelta(seconds=remaining))
    else:
        est_time = ''
    
    if est_time != '':    
        est_time = ' (' + str(est_time[:est_time.find('.')]) + ' remaining)'
        
    length = 50 - len(est_time) - len(prefix) - len(suffix)
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {est_time}', end = printEnd)
    #print('\r%s|%s| %s%% %s%s' % (prefix, bar, percent, suffix, est_time), end = printEnd, flush = True)
    # Print New Line on Complete
    if iteration == total: 
        print()

    
if __name__ == '__main__':
    main()    
