"""
Created on Thu Apr 30 12:04:19 2020

Author: Spencer Ferguson-Dryden
https://github.com/sfergusond

TO DO: Implement description-only upload, migrate helper functions out, add Facebook, Apple, Email/PW login options

Uses: webbot from https://github.com/nateshmbhat/webbot
"""

from webbot import Browser
import datetime
import time
from bs4 import BeautifulSoup

strava_activity_types = ['Ride', 'Run', 'Swim', 'Hike', 'Walk', 'AlpineSki', 'BackcountrySki', 'Canoeing', 'Crossfit',  'EBikeRide', 'Elliptical', 'Handcycle', 'IceSkate', 'InlineSkate', 'Kayaking', 'Kitesurf', 'NordicSki', 'RockClimbing', 'RollerSki', 'Rowing', 'Snowboard', 'Snowshoe', 'StairStepper', 'StandUpPaddling', 'Surfing', 'Velomobile', 'VirtualRide', 'VirtualRun', 'WeightTraining', 'Wheelchair', 'Windsurf', 'Workout', 'Yoga']

r2w_run_types = ['VO2 Max', 'Endurance', 'Steady State', 'Hill Training', 'Tempo', 'Fartlek', 'Recovery', 'Speed Training', 'Threshold', 'wu/cd', 'Interval Workout', 'Race'] 

r2w_activity_types = ['Aqua Jogging', 'Cycling', 'Elliptical', 'Hiking', 'Cross Training/Other', 'Other', 'NO RUN - OFF']

def login_strava(username, password, web):
    web.go_to('https:///www.strava.com/login')
    web.click('Log in using Google')
    web.type(username, into = 'Email or phone')
    web.click('Next')
    time.sleep(2)
    web.type(password, classname = 'Xb9hP')
    web.click('Next')
    time.sleep(1)

def login_r2w(username, password, web):
    web.go_to('https://www.running2win.com/')
    web.click('LOG IN')
    time.sleep(2) # Prevent username from failing to enter
    web.type(username, into='Username')
    web.click('NEXT' , tag='span')
    web.type(password, into='Password')
    web.click('Login')
    
def log_to_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    runs = soup.find_all("table", class_ ='encapsule')
    
    '''with open('runs.txt', 'w') as f:
        print(runs, file = f)'''
        
    return str(runs)

def get_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(' | ', strip = True)
    return text

def runs_to_dict(text):
    text = text[83:]
    
    text = text[text.find('| , |'):]
    runs = text.split('| , |')
    runs = runs[1:]
        
    master_list = []
        
    for r in runs:
        #print(r)
        # date
        date = r[r.find('y,') + 3:r.find(' |')]
    
        # title and type
        r = r[r.find(' |') + 1:]
        title = r[2:r.find(' |')]
        r = r[r.find(' |') + 3:]
        _type = r[:r.find(' |')] 
        title += ' ' + _type
        if _type == r2w_activity_types[-1] or _type == r2w_activity_types[-2] or _type == r2w_activity_types[-3]: continue;
            
        # distance
        r = r[r.find('distance |') + 11:]
        distance = r[:r.find(' |'):]
        if '-' in distance: continue;
            
        # time
        if ':' in distance:
            r = r[r.find('in'):]
            time = r[3:r.find(' [')]
        else: time = '0'
            
        # description
        r = r[r.find('| Comments |') + 13:]
        description = r[:r.find(' |')]
        if description == 'Private Notes': description = ' '; # check for empty description
    
        if 'Race Information:' in r:
            description += parse_race(r[r.find('Race Information:') + 31:r.find('| more...')])
            
        if 'Interval Information:' in r:
            description += parse_intervals(r[r.find('Interval Information'):r.find('| more...')])
            
        r = r[r.find('| Workout Comments by Members') + 29:r.find('| Add Workout Comment')] # check for comments
        if len(r) > 1:
            description += parse_comments(r)
    
        # add to dict
        _dict = {'date': parse_date(date), 'type': _type, 'title': title, 'distance': str(parse_distance(distance)), 'time': parse_time(time), 'description': description}
        #print(_dict)
        master_list.append(_dict)
        
    '''for i in master_list:
        print(i, end = '\n\n')'''
        
    return master_list

def parse_intervals(r): # not yet implemented
    r = r[r.find('1 |'):]
    desc = ''
    grid = r.split(' | ')
    #print(grid)
    
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
    import re
    unit = distance[distance.find(' ') + 1:]
    dist = distance[:distance.find(' ')]
    #dist = re.sub("[^0-9]", "", dist)
    
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

def add_strava_entry(run, web):
    #web.click(id='activity_distance')
    web.type(run['distance'], id='activity_distance')
    
    web.click('NEXT', tag = 'span')
    
    web.type(run['time'][0], id='activity_elapsed_time_hours')
    web.type(run['time'][1], id='activity_elapsed_time_minutes')
    web.type(run['time'][2], id='activity_elapsed_time_seconds')
    
    web.click(id='activity-type-dd')
    if run['type'] in r2w_run_types or 'Run' in run['type']:
        web.click('Run', tag='a')
    elif run['type'] == 'Hiking':
        web.click('Hike')
    elif run['type'] == 'Cycling':
        web.click('Ride')
    elif run['type'] == 'Elliptical':
        web.click('Elliptical')
    else:
        web.click('Workout')

    web.click('NEXT', tag='span')
    web.type(run['date'], id='activity_start_date')
    web.click('NEXT', tag='span')
    
    web.type(run['title'], id='activity_name')
    
    if 'Long' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Long Run')
    elif 'Race' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Race')
    elif 'VO2 Max' in run['type'] or 'Endurance' in run['type'] or 'Steady State' in run['type'] or 'Tempo' in run['type'] or 'Hill Training' in run['type'] or 'Fartlek' in run['type'] or 'Speed Training' in run['type'] or 'Threshold' in run['type'] or 'Interval' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Workout')
    
    web.type(run['description'], id='activity_description')
    
    web.click(xpath='/html/body/div[1]/div[3]/div[1]/form/div[6]/div/input')

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Retrieve R2W data and upload to Strava -- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru \"myr2wusername\" ---')
    parser.add_argument('-ru', type = str, metavar = 'r2w_username', help = 'Running2Win username', required=True)
    parser.add_argument('-rp', type = str, metavar = 'r2w_password', help = 'Running2Win password', required=True)
    parser.add_argument('-a', type = str, metavar = 'after_date', help = 'Date after which to search for activities on Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--', required=True)
    parser.add_argument('-b', type = str, metavar = 'before_date', help = 'Date at which to stop collecting activities form Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--', required=True)
    parser.add_argument('-su', type = str, metavar = 'strava_email (MUST BE A GOOGLE EMAIL ADDRESS LINKED TO YOUR STRAVA ACCOUNT)', help = 'Strava username', required=True)
    parser.add_argument('-sp', type = str, metavar = 'strava_password', help = 'Strava password', required=True)
    args = parser.parse_args()
            
    web = Browser(showWindow=False)
    login_r2w(args.ru, args.rp, web)
    tmp = (args.a).split('-')
    start = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    tmp = (args.b).split('-')
    end = datetime.date(int(tmp[0]),int(tmp[1]), int(tmp[2]))
    delta = datetime.timedelta(weeks=8)
    runs = []
    
    # Navigate to running log
    while start < end:
        upper = start + delta
        if upper > end:
            upper = end
        web.go_to('https://www.running2win.com/community/view-member-running-log.asp?sd='+ str(start) + '&ed=' + str(upper))
        start += delta + datetime.timedelta(days=1)
        
        file = web.get_page_source() # convert to html
        f = log_to_html(file) # store as text/text file
        #log_to_html(file)
        t = get_text(f) # strip text
        '''with open('runs.txt', 'r') as f:
            t = get_text(f)'''
        
        gathered = runs_to_dict(t)
        runs.extend(gathered)
        print('Gathered', len(gathered), '| Total:', len(runs), '| Most Recent:', gathered[-1]['date'])
    
    login_strava(args.su, args.sp, web)
    
    count = 0
    for i in runs:
        pct_done = int(count/len(runs)*100)
        web.go_to('https://www.strava.com/upload/manual')
        add_strava_entry(i, web)
        count += 1
        if count % 10 == 0:
            print('Added 10 activities to Strava | Total =', count, 'of', len(runs), f'({pct_done}%)')
        
    web.driver.close()
    print('Successfully added', count,' activities to Strava')
    