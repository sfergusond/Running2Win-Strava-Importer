"""
Created on Thu Apr 30 12:04:19 2020

Author: Spencer Ferguson-Dryden
https://github.com/sfergusond

TO DO: Implement description-only upload

Features
    Gathers all activity data from Running2Win, including non-running activities such as Cross Training, NO RUN - OFF, and Other activity types. Activites will be gather beginning from the specified begin date to the specified end date.
    For each activity, the following information is retrieved:
        Date
        Distance
        Time
        Activity Type
        Activity Title
        And, if they exist:
            Description (private notes not included)
            Difficulty
            Average HR
            Max HR
            Race Information
            Interval Information
            Member Comments
    If csv is entered in the upload/csv prompt, then all gathered activities will be downloaded to a CSV file in the same directory as the downloaded program.
    If upload is entered in the upload/csv prompt, then all gathered activities will be uploaded to Strava


Uses: webbot from https://github.com/nateshmbhat/webbot
"""
import os
import sys

def main():
    if len(sys.argv) == 1:
        print(sys.argv[0] + ' ARGV')
        os.system('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py')
        os.system('python get-pip.py')
        os.system('pip install -r requirements.txt')
    
    args = {}
    
    print('\nStarting R2W Importer\n\nPlease fill out the following fields and hit ENTER on your keyboard after typing each entry.\nEnter options exactly as they appear.')
    
    ru = str(input('Enter your Running2Win username: '))
    args['ru'] = ru
    rp = str(input('Enter your Running2Win password: '))
    args['rp'] = rp
    a = str(input('Enter date of first activity to collect (format: YYYY-MM-DD): '))
    args['a'] = a
    b = str(input('Enter date of last activity to collect (format: YYYY-MM-DD): '))
    args['b'] = b
    c = str(input('Would you like to download to a .csv file or upload to Strava? (Type one of the follow and enter: csv | upload ): '))
    args['c'] = c
    if c != 'csv':
        m = str(input('How do you login to Strava? (Type one of the following and enter: google | facebook | email ): '))
        args['m'] = m 
        if m == 'google':
            su = str(input('Enter Google account email: '))
            args['su'] = su
            sp = str(input('Enter Google account password: '))
            args['sp'] = sp
        elif m == 'facebook':
            su = str(input('Enter Facebook account email: '))
            args['su'] = su
            sp = str(input('Enter Facebook account password: '))
            args['sp'] = sp
        else:
            su = str(input('Enter Strava account email: '))
            args['su'] = su
            sp = str(input('Enter Strava account password: '))
            args['sp'] = sp
            
    print('')
    # Run!
    driver(args)
    
from webbot import Browser
import datetime
import time
from bs4 import BeautifulSoup
import r2w_parser

def login_strava(username, password, web, method):
    web.go_to('https:///www.strava.com/login')
    if method == "google":
        print('Logging into Strava with Google...')
        web.click('Log in using Google')
        web.type(username, into = 'Email or phone')
        web.click('Next')
        time.sleep(3)
        web.type(password, classname = 'Xb9hP')
        web.click('Next')
    elif method == 'facebook':
        print('Logging into Strava with Facebook...')
        web.click('Log in using Facebook')
        web.type(username, id='email')
        web.type(password, id='pass')
        web.click(id='loginbutton')
    else:
        print('Logging into Strava with email/password...')
        web.type(username, id='email')
        web.type(password, id='password')
        web.click(id='login-button')
    print('Successfully logged into Strava and beginning activity upload...\n')
    time.sleep(5)

def login_r2w(username, password, web):
    web.go_to('https://www.running2win.com/')
    web.click('LOG IN')
    time.sleep(2) # Prevent username from failing to enter
    print('Logging into Running2Win...')
    web.type(str(username), into='Username')
    web.click('NEXT' , tag='span')
    web.type(str(password), into='Password')
    web.click('Login')
    print('Successfully logged into Running2Win and beginning activity download...\n')

def add_strava_entry(run, web):
    # DISTANCE
    web.type(run['distance'], id='activity_distance')
    
    # TIME
    web.type(run['time'][0], id='activity_elapsed_time_hours')
    web.type(run['time'][1], id='activity_elapsed_time_minutes')
    web.type(run['time'][2], id='activity_elapsed_time_seconds')
    
    # TYPE
    web.click(id='activity-type-dd')
    if run['type'] in r2w_parser.r2w_run_types or 'Run' in run['type']:
        web.click('Run', tag='a')
    elif run['type'] == 'Hiking':
        web.click('Hike')
    elif run['type'] == 'Cycling':
        web.click('Ride')
    elif run['type'] == 'Elliptical':
        web.click('Elliptical')
    elif run['type'] in r2w_parser.strava_activity_types:
        scroll = r2w_parser.strava_activity_types.index(run['type'])
        _type = r2w_parser.strava_activity_types[scroll]
        web.scrolly(5)
        if scroll > 9:
            web.scrolly(5*scroll)
        web.click(_type)
    else:
        web.click('Workout')
        
    # DATE
    web.type(run['date'], id='activity_start_date')
    web.click('NEXT', tag='span')
    
    # TITLE
    web.type(run['title'], id='activity_name')
    
    # RUN SUBTYPE
    if 'Long' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Long Run')
    elif 'Race' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Race')
    elif 'VO2 Max' in run['type'] or 'Endurance' in run['type'] or 'Steady State' in run['type'] or 'Tempo' in run['type'] or 'Hill Training' in run['type'] or 'Fartlek' in run['type'] or 'Speed Training' in run['type'] or 'Threshold' in run['type'] or 'Interval' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Workout')
    
    # DESCRIPTION
    web.type(run['description'], id='activity_description')
    
    # DIFFICULTY
    if run['difficulty'] > 1:
        web.click(id='perceived-exertion-slider-1')
        for i in range(run['difficulty']):
            web.press(web.Key.RIGHT)
        web.click('NEXT', tag = 'span')
        
    # SUBMIT
    web.click(xpath='/html/body/div[1]/div[3]/div[1]/form/div[6]/div/input')
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 2, length = 100, fill = '█', printEnd = "\r"):
    """
    Borrowed from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def driver(args):
    import sys
    web = Browser(showWindow=False)
    
    print('Loading https://www.running2win.com ...')
    login_r2w(args['ru'], args['rp'], web)
    
    tmp = (args['a']).split('-')
    start = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    tmp = (args['b']).split('-')
    end = datetime.date(int(tmp[0]),int(tmp[1]), int(tmp[2]))
    delta = datetime.timedelta(weeks=8)
    
    # helpers for progress bar
    total_days_str = str(end - start)
    if 'day' not in total_days_str: total_days = 1
    else: total_days = int(total_days_str[0:total_days_str.find(' day')])
    
    runs = [] # Master list for activities
    
    # Navigate to running log and iterate through 8 week chunks
    count = 0
    while start < end:
        count += 56
        upper = start + delta
        if upper > end:
            upper = end
            count = total_days
        web.go_to('https://www.running2win.com/community/view-member-running-log.asp?sd='+ str(start) + '&ed=' + str(upper))
        start += delta + datetime.timedelta(days=1)
        
        file = web.get_page_source() # convert to html
        f = r2w_parser.log_to_html(file) # store html as text/text file
        t = r2w_parser.get_text(f) # strip text
        gathered = r2w_parser.runs_to_dict(t, f)
        runs.extend(gathered)
        
        progress = f'Gathered {len(runs)} activities | Most Recent: ' + gathered[0]['date']
        printProgressBar(count, total_days, prefix=progress)
        
    if args['c'] == 'csv':
        import pandas as pd
        for a in runs:
            tmp = a['time']
            if tmp[0] == 0:
                time = f'{tmp[1]}:{tmp[2]}'
            else:
                time = f'{tmp[0]}:{tmp[1]}:{tmp[2]}'
            a['time'] = time
    
        pd.DataFrame(runs).to_csv('activities.csv', index=False)
        print('\nActivities downloaded to \"activities.csv\" in the program\'s folder')
        web.driver.close()
    
    print("\nLoading https://www.strava.com ...")
    login_strava(args['su'], args['sp'], web, args['m'])
    
    count = 0
    for i in runs:
        web.go_to('https://www.strava.com/upload/manual')
        add_strava_entry(i, web)
        
        count += 1
        progress = f'Added activity on ' + i['date'] + f' to Strava | Total = {count} of {len(runs)}'
        printProgressBar(count, len(runs), prefix=progress)
        
    web.driver.close()
    print(f'\nSuccessfully added {count} activities to Strava!')
    
if __name__ == '__main__':
    main()    