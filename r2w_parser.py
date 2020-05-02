# -*- coding: utf-8 -*-
"""
Author: Spencer Ferguson-Dryden
https://github.com/sfergusond

Helper functions for R2WImporter

Uses: webbot from https://github.com/nateshmbhat/webbot
"""
import datetime
from bs4 import BeautifulSoup

strava_activity_types = ['Ride', 'Run', 'Swim', 'Hike', 'Walk', 'Alpine Ski', 'BackcountrySki', 'Canoeing', 'Crossfit',  'EBikeRide', 'Elliptical', 'Handcycle', 'Ice Skate', 'Inline Skate', 'Kayaking', 'Kitesurf', 'Nordic Ski', 'Rock Climbing', 'Roller Ski', 'Rowing', 'Snowboard', 'Snowshoe', 'Stair-Stepper', 'Stand Up Paddling', 'Surfing', 'Velomobile', 'Virtual Ride', 'Virtual Run', 'Weight Training', 'Wheelchair', 'Windsurf', 'Workout', 'Yoga']

r2w_run_types = ['VO2 Max', 'Endurance', 'Steady State', 'Hill Training', 'Tempo', 'Fartlek', 'Recovery', 'Speed Training', 'Threshold', 'wu/cd', 'Interval Workout', 'Race'] 

r2w_activity_types = ['Aqua Jogging', 'Cycling', 'Elliptical', 'Hiking', 'Cross Training/Other', 'Other', 'NO RUN - OFF']

r2w_xt_types = ['Core (general)', 'Sit-ups', 'Push-ups', 'Swimming', 'Biking', 'Hiking', 'Skiing', 'Mountain Biking', 'Walking', 'Elliptical', 'Weights (general)', 'Circuits', 'Rollerblading', 'Skating', 'Pilates', '[General]']

def log_to_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    runs = soup.find_all("table", class_ ='encapsule')
        
    return str(runs)

def get_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(' | ', strip = True)
    return text

def runs_to_dict(html, soup):
    html = html[83:]
    
    html = html[html.find('| , |'):]
    runs = html.split('| , |')
    runs = runs[1:]
    
    master_list = []
    interval_count = 0
    
    s = BeautifulSoup(soup, 'lxml')
    interval_tables = s.find_all(string = 'Interval Information:')
        
    for r in runs:
        # date
        date = r[r.find('y,') + 3:r.find(' |')]
    
        # title and type
        r = r[r.find(' |') + 1:]
        title = r[2:r.find(' |')]
        r = r[r.find(' |') + 3:]
        _type = r[:r.find(' |')] 
        title += ' ' + _type
            
        # distance
        r = r[r.find('distance |') + 11:]
        distance = r[:r.find(' |'):]
        if '-' in distance: distance = '0.01';
        else: distance = str(parse_distance(distance));
            
        # time
        if ':' in distance:
            r = r[r.find('in'):]
            time = r[3:r.find(' [')]
        else: time = '0'
            
        # description
        r = r[r.find('| Comments |') + 13:]
        description = r[:r.find(' |')]
        if description == 'Private Notes': description = ' '; # check for empty description
        
        # difficulty
        difficulty = 1
        r = r[r.find('[Rating: ') + 9:]
        difficulty = int(r[:r.find(']')])
        
        if _type == 'Cross Training/Other' or _type == 'Other':
            r = r[r.find('Cross Training Info: |') + 56:]
            xt_type = r[:r.find(' |')]
            if xt_type == 'Weights (general)': _type = 'Weight Training'
            elif xt_type == 'Swimming': _type = 'Swim'
            elif xt_type == 'Skating': _type = 'Ice Skate'
            elif xt_type == 'Rollerblading': _type = 'Inline Skate '
            elif xt_type == 'Walking': _type = 'Walk'
            elif xt_type == 'Pilates': _type = 'Yoga'
            elif xt_type == 'Skiing': _type = 'Alpine Ski'
            title += f' - {xt_type}'
            description += parse_xt(r)
    
        if 'Race Information:' in r:
            description += parse_race(r[r.find('Race Information:') + 31:r.find('| more...')])
            
        if 'Interval Information:' in r:
            description += '\n' + parse_intervals(interval_tables[interval_count])
            interval_count += 1
        
        # HR data
        r = r[r.find('Average HR | ') + 13:]
        avg_hr = r[:r.find(' |')]
        r = r[r.find('MAX HR | ') + 9:]
        max_hr = r[:r.find(' |')]
        
        # member comments
        r = r[r.find('| Workout Comments by Members') + 29:r.find('| Add Workout Comment')]
        if len(r) > 1:
            description += parse_comments(r)
    
        # add to dict
        _dict = {'date': parse_date(date), 'type': _type, 'title': title, 'distance': distance, 'time': parse_time(time), 'description': description, 'difficulty': difficulty, 'avg_hr': avg_hr, 'max_hr': max_hr}
        #print(_dict)
        master_list.append(_dict)
        
    return master_list

def parse_xt(r):
    desc = '\n Cross-training type: '
    desc += r[:r.find(' |')] 
    
    desc += '\n Description: '
    
    r = r[r.find(' | ') + 3:]
    r = r[r.find(' |' ) + 3:]
    
    desc += r[:r.find(' |')]
    
    desc += '\n Comments :'
    
    r = r[r.find('Cross Training Comments: | ') + 27:]
    
    desc += r[r.find(' |')]
    
    return desc

def parse_intervals(table): 
    desc = ''
    intervals = table.parent.parent.parent
    
    rows = intervals.tbody.find_all("tr")
    cols = intervals.find_all("td")
    headings = []
    
    for td in rows[0].find_all("td"):
        headings.append(td.text.replace('\n', ' ').strip())
        
    #print(headings)
    rows = rows[1:]
    table = []
    
    for r in rows:
        cols = r.find_all("td")
        tmp = []
        for c in cols:
            tmp.append(c.text.replace('\n', '').strip())
            #print(c.text)
        table.append(tmp)
    #print(table)
    
    tmp = ' | '.join(['{:^1}'.format(i) for i in headings])
    desc += tmp + '\n'

    for r in table:
        tmp = ' | '.join(['{:^1}'.format(i) for i in r]) + '\n'
        desc += tmp

    return desc         

def parse_race(r):  
    name = r[:r.find(' |')]
    r = r[r.find('Distance |') + 11:]
    if name == 'Terrain': name = '';
    
    distance = r[:r.find(' |')]
    r = r[r.find('Time |') + 7:]
    if distance == 'Time': distance = '';
    
    time = r[:r.find(' |')]
    r = r[r.find('Race Splits | ') + 13:]
    if time == 'Race Splits': time = '';
    if '(relay split)' in time: time = time[:time.find(' (relay split)')]
    
    splits = r[:r.find(' |')]
    r = r[r.find('Overall Place |') + 15:]
    if splits == ' Cool Down': splits = '';
    
    unit = distance[distance.find(chr(0xa0)) + 1:]
    if 'Mile' in unit:
        pace_per_mile = parse_time(time, True)/float(distance[:distance.find(chr(0xa0))])
    elif 'Kilo' in unit:
        pace_per_mile = parse_time(time, True)/(float(distance[:distance.find(chr(0xa0))]) * 0.621371)
    elif 'Meter' in unit:
        pace_per_mile = parse_time(time, True)/(float(distance[:distance.find(chr(0xa0))]) * 0.000621371)
    else:
        pace_per_mile = parse_time(time, True)/(float(distance[:distance.find(chr(0xa0))]) * 0.000568182)
    mm = int(pace_per_mile//60)
    ss = round(pace_per_mile % 60, 2)
    pace_per_mile = str(mm) + ':' + str(ss)
    
    place = r[:r.find(' |')]
    r = r[r.find('Comments |') + 10:]
    if place == 'Age Place': place = '';
    
    comments = r
    
    desc = f'\n\nRace Information:\n\nRace Name: {name}\nDistance: {distance}\nTime: {time}\nPace per Mile: {pace_per_mile}\nSplits: {splits}\nPlace: {place}\nComments: {comments}'
    
    return desc
        
def parse_comments(r):
    desc = '\n\nComments:\n\n'
    r = r[r.find('Action |') + 8:]
    #print(r)
    while len(r) > 0:
        desc += '(' + r[1:r.find(' |')] + '): '
        r = r[r.find(' |') + 3:]
        desc += r[:r.find(' |')] + '\n'
        if ' |' in r:
            r = r[r.find(' |') + 2:]
        else: break;
    return desc

def parse_distance(distance):
    unit = distance[distance.find(' ') + 1:]
    dist = distance[:distance.find(' ')]
    
    if 'Mile' in unit:
        return round(float(dist), 2)
    elif 'Kilo' in unit:
        return round(float(dist) * 0.621371, 2)
    elif 'Meter' in unit:
        return round(float(dist) * 0.000621371, 2)
    else:
        return round(float(dist) * 0.000568182, 2)
    

def parse_time(time, seconds = False):
    time = time.split(':')
    
    if len(time) == 1:
        time = [str(0), str(0), time[0]]
    elif len(time) == 2:
        time = [str(0), time[0], time[1]]
       
    if seconds == True: 
        return 3600*int(time[0]) + 60*int(time[1]) + float(time[2]) 
    return time  
    
def parse_date(date):
    from dateutil import parser
    
    d = parser.parse(date)
    d = d.strftime("%m/%d/%Y")
    
    return d
