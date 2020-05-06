# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 18:14:00 2020

@author: sferg
"""

import csv
import webbot_exe
import stravalib
import time

STRAVA_CLIENT_ID = '47270'
STRAVA_CLIENT_SECRET = '392e9cc577c84cb9e54370ee9bd98be5885cd30b'
ACCESS_TOKEN = None
CLIENT = None

# maybe replace with stravalib version? Or manufacture HTTP requests manually?
def initialize_client(url = None, web = None, scope = '', CLIENT_ID = STRAVA_CLIENT_ID, CLIENT_SECRET = STRAVA_CLIENT_SECRET):
    
    _client = stravalib.Client()
    auth_url = _client.authorization_url(client_id=CLIENT_ID, redirect_uri='https://localhost:8000', approval_prompt='force', scope = scope)
    
    web.go_to(auth_url)
    web.click(id='authorize')
    
    print('Authorizing R2WImporter access...\n')
    
    time.sleep(4)
    
    auth_url = web.get_current_url()
    auth_code = auth_url[auth_url.find('code=')+5:auth_url.find('&scope')]
    
    token = _client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=auth_code).get('access_token')
    
    return stravalib.Client(access_token=token)

# Args: date (yyyy-mm-dd) from which to begin activity list
# return: list of dicts of all runs since the specified date
# keeps only athlete, distance, elapsed_time, elev_high, elev_low, max_speed, moving_time, name, total_elevation_gain, and start_date_local
# auto filter for type == 'Run' and length > 4.8km
def activities(date_after, date_before, client = None, keep = None, token = None):
    runs = client.get_activities(before=date_before, after=date_after)
    
    li = []
    
    if keep == None:
        keep = ['distance', 'elapsed_time', 'elev_high', 'elev_low', 'max_speed', 'moving_time', 'name', 'total_elevation_gain', 'date', 'id', 'description']
    else:
        keep = keep
    
    for a in runs:
        # Convert each Activity Summary to type dict
        run = a.to_dict()
        
        # skip if activity is not a run
        if run['type'] != 'Run':
            continue
        
        # convert date to friendly format
        t = run['start_date_local']
        #t = t.strftime('%Y-%m-%d')
        run['date'] = t[0:10]
        
        # Filter excess attributes
        for k in list(run.keys()):
            if k not in keep:
                del run[k]  

        run['id'] = a.id # fix for stravalib compatibility
        li.append(run)
        
    return li

def get_run(filter_by, term, runs):
    if filter_by == 'index':
        return runs[term]
    
    li = []
    for a in runs:
        if a[str(filter_by)] == term:
            li.append(a)
            
    if len(li) == 0: return 'ERROR: no run found'
    else: return li
    
def runs_to_txt(runs):
    with open("runs.txt", "w", encoding = 'utf-16') as f:
        print(runs, file = f)
        
def runs_to_csv(runs):
    with open('intensity.csv', 'w', newline = '') as f:
        fieldnames = ['date', 'intensity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for x in runs:
            writer.writerow(x)
            
if __name__ == '__main__':
    initialize_client()
            
            