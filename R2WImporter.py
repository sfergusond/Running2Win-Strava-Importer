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

TO DO: TIME ESTIMATE

Uses: webbot from https://github.com/nateshmbhat/webbot
"""
import webbot_exe
from webbot_exe import Browser
import datetime
import time
import r2w_parser
import R2WImportComments
import pandas as pd

def main():
    args = {}
        
    print('\nStarting R2W Importer\n\nPlease fill out the following fields and hit ENTER on your keyboard after typing each entry.\n')
    
    valid = False
    while not valid:
        a = str(input('\nEnter date of first activity to collect (format: YYYY-MM-DD)\n> '))
        valid = validate_date(a)
    args['a'] = a
        
    valid = False
    while not valid:
        b = str(input('Enter date of last activity to collect (format: YYYY-MM-DD)\n> '))
        valid = validate_date(b, a)
    args['b'] = b
    
    valid = False
    while not valid:
        c = str.lower(str((input('\nChoose what you want to do with your Running2Win data.\n\n * csv = just download your data to a csv file\n\n * upload = just upload your R2W data to Strava\n\n * both = download a csv and upload data to Strava\n\n * comments = update existing activites on Strava with comments/notes/descriptions from Running2Win (activities missing from Strava will also be uploaded)\n\nType one of the following and enter: csv | upload | both | comments \n> '))))
        if c == 'csv' or c == 'upload' or c == 'both' or c == 'comments':
            valid = True
    args['c'] = c

    if 'comments' in c:
        print('\nYou\'ve chosen to upload comments from R2W to existing Strava activites. Please choose upload policies.\n')
        
        valid = False
        while not valid:
            p1 = str.lower(str((input('For a given day, if the incoming activity from Running2Win does not match the distance of any activities of that day on Strava, would you like to create a new activity or append the incoming description to the first existing activity on Strava?\nType one of the following: create | append\n> '))))
            if p1 == 'create' or p1 == 'append':
                valid = True
        args['p1'] = p1
            
        p2 = str((input('\nIn meters, type how strict the matching policy should be. (i.e.  100  would only consider a R2W activity and a Strava activity a match if the difference of their distances is +/- 100 meters)\n> ')))
        while not p2.isdecimal():
            p2 = str(input('Type a whole number, in meters\n> '))
        args['p2'] = int(p2)
        
    print()
    
    # Run!
    # DEBUG test = {'a':'2020-01-01', 'b':'2020-05-05', 'c':'comments', 'p1':'append','p2':'create'}
    driver(args)
    return

def validate_date(date, s = None):
    d = date.split('-')
    
    if len(d) < 3: 
        print('Invalid input')
        return False
    try:
        yr = int(d[0])
    except:
        print('Invalid year')
        return False
    try:
        mo = int(d[1])
    except:
        print('Invalid month')
        return False   
    try:
        day = int(d[2])
    except:
        print('Invalid day')
        return False 
    
    if yr < 1980:
        print('Invalid year')
        return False
    if mo < 1 or mo > 12:
        print('Invalid month')
        return False
    if day < 1 or day > 31:
        print('Invalid day')
        return False
    
    if s != None:
        start = s.split('-')
        start = datetime.date(int(start[0]),int(start[1]), int(start[2]))
        end = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        dif = str(end-start)
        if 'day' not in dif: return True
        dif = int(dif[:dif.find(' day')])
        if dif < 0:
            print('End date must be later than start date')
            return False
        
    return True
    

def login_strava(web):
    web.go_to('https:///www.strava.com/login')
    print('\nHow do you login to Strava? Google | Facebook | Apple | Email')
    method = str.lower(input(('\n> ')))
    if "google" in method:
        print('\nLogging into Strava with Google...')
        web.click('Log in using Google')
        time.sleep(3)
        
        user = input('\nEnter your Google account email\n> ')
        web.type(user, id='identifierId')
        
        web.press(web.Key.ENTER)
        time.sleep(2)
        
        pw = input('Enter your Google account password\n> ')
        web.type(pw, into='Enter your password')
        
        web.press(web.Key.ENTER)
    elif 'facebook' in method:
        print('\nLogging into Strava with Facebook...')
        web.click('Log in using Facebook')
        time.sleep(3)
        
        user = input('\nEnter your Facebook account email\n> ')
        web.type(user, id='email')
        pw = input('Enter your Facebook account password\n> ')
        web.type(pw, id='pass')
        
        web.click(id='loginbutton')
    elif 'email' in method:
        print('\nLogging into Strava with email/password...')
        user = input('\nEnter your Strava account email\n> ')
        web.type(user, id='email')
        pw = input('Enter your Strava account password\n> ')
        web.type(pw, id='password')
        web.click(id='login-button')
        
        time.sleep(5)
        if len(web.find_elements(text = 'The username or password did not match. Please try again.')) != 0: 
             print('Login failed. Please try again.\n')
             login_strava(web)
    else:
        print('\nLogging into Strava with Apple ID')
        web.click(id='apple-signin')
        time.sleep(3)
        
        user = input('\nEnter your Apple ID\n> ')
        web.type(user, id='account_name_text_field')
        
        web.click(id='sign-in')
        time.sleep(1)
        
        pw = input('Enter your Apple account password\n> ')
        web.type(pw, id='password_text_field')
        
        web.click(id='sign-in')
        
    time.sleep(5)
    if 'strava.com' in web.get_current_url()[0:24]: # ATTEMPT 1
        print('Successfully logged into Strava and beginning activity upload...\n')
        return web
    else:
        print(input('\nCHECK YOUR PHONE FOR POTENTIAL TWO-FACTOR VERIFICATION PROMPT\n\nPress verification prompt on your phone or enter validation code here and press ENTER to continue\n> '))
        time.sleep(7)
        if 'strava.com' in web.get_current_url()[0:24]:
            print('Successfully logged into Strava and beginning activity upload...\n')
            web.switch_to_tab(number = 1)
            return web
        else: # ATTEMPT 2
            web.scrolly(200)
            web.click('verification')
            time.sleep(7)
            web.type(str(input('\nCHECK YOUR PHONE FOR POTENTIAL TWO-FACTOR VERIFICATION PROMPT\n\nPress verification prompt on your phone or enter validation code here and press ENTER to continue\n> ')), into='Enter the code')
            web.press(web.Key.ENTER)
            time.sleep(5)
            if 'strava.com' not in web.get_current_url()[0:24]: # MANUAL ATTEMPT
                web.driver.close()
                tmp = Browser(showWindow = True)
                tmp.go_to('https://www.strava.com/login')
                print(input('Issue logging in. Please login manually and press ENTER when done'))
                time.sleep(5)
                tmp.driver.set_window_position(-10000, 0)
                return tmp
            else:
                print('Successfully logged into Strava and beginning activity upload...\n')
                web.switch_to_tab(number = 1)
                return web

def login_r2w(web):
    print('Loading Running2Win...\n')
    web.go_to('https://www.running2win.com/')
    web.click('LOG IN')
    time.sleep(2) # Prevent username from failing to enter
    
    web.type(input('Enter your Running2Win username\n> '), into='Username')
    web.type(input('Enter your Running2Win password\n> '), into='Password')
    '''DEBUGweb.type("F  D", into='Username')
    web.type('Orange%ID', into='Password')'''
    web.click('Login')

    time.sleep(5)
    if len(web.find_elements(text = 'Invalid login. Please try again.')) == 0:
        print('\nSuccessfully logged into Running2Win and beginning activity download...\n')
    else:
        print('Login failed. Please try again.\n')
        login_r2w(web)

def add_strava_entry(run, web):
    web.go_to('https://www.strava.com/upload/manual')
    
    # DISTANCE
    web.type(str(run['distance']), id='activity_distance')
    
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
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 25, fill = '█', printEnd = '\r', t1 = None, t2 = None, step = 1):
    """
    Borrowed from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """    
    if t1 != None and t2 != None:
        if iteration < total:
            remaining = (t2-t1)*((total/step) - (iteration/step))
        else: remaining = 0
        est_time = str(datetime.timedelta(seconds=remaining))
    else:
        est_time = '0:00:00.'
        
    est_time = est_time[:est_time.find('.'):]
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print(f'\r{est_time} remaining {prefix} |{bar}| {percent}% {suffix}', end = printEnd, flush = True)
    #print('\r%s remaining %s|%s| %s%% %s' % (est_time, prefix, bar, percent, suffix), end = printEnd, flush = True)
    # Print New Line on Complete
    if iteration == total: 
        print()

def to_csv(runs):
    for a in runs:
        tmp = a['time']
        if tmp[0] == 0:
            t = f'{tmp[1]}:{tmp[2]}'
        else:
            t = f'{tmp[0]}:{tmp[1]}:{tmp[2]}'
        a['time'] = t
    
    pd.DataFrame(runs).to_csv('activities.csv', index=False)
    print('\nActivities downloaded to \"activities.csv\" in the program\'s folder')
    
def r2w_download(start, end, web):
    li = []
    
    tmp = start.split('-')
    start = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    tmp = end.split('-')
    end = datetime.date(int(tmp[0]),int(tmp[1]), int(tmp[2]))
    
    # Init iterator and progress bar helpers
    delta = datetime.timedelta(weeks=8)
    total_days_str = str(end - start)
    if 'day' not in total_days_str: total_days = 1
    else: total_days = int(total_days_str[0:total_days_str.find(' day')])
    
    # Navigate to R2W running log and iterate through 8 week chunks
    count = 0
    
    while start < end:
        t1 = time.time()
        
        count += 56
        upper = start + delta
        if upper > end:
            upper = end
            count = total_days
        url = 'https://www.running2win.com/community/view-member-running-log.asp?sd='+ str(start) + '&ed=' + str(upper)
        time.sleep(5)
        web.go_to(url)
        start += delta + datetime.timedelta(days=1)
        
        file = web.get_page_source() # convert to html
        f = r2w_parser.log_to_html(file) # store html as text/text file
        t = r2w_parser.get_text(f) # strip text
        gathered = r2w_parser.runs_to_dict(t, f)
        li.extend(gathered)
        
        t2 = time.time()
        progress = f'| Gathered {len(li)} activities | Most Recent: ' + gathered[0]['date']
        printProgressBar(count, total_days, suffix = progress, t1 = t1, t2 = t2, step = 56)
    
    return li

def driver(args):       
    web = Browser(showWindow=False)
    login_r2w(web)
    
    # Master list of R2W activities
    runs = r2w_download(args['a'], args['b'], web) 
        
    if 'comments' in args['c']: 
        return R2WImportComments.main(runs, web, args['a'], args['b'], args['p1'], args['p2']) # let R2WImportComments handle the rest
        
    # CSV download
    if 'csv' in args['c']:
        to_csv(runs)
        web.driver.close()
        return
    elif 'both' in args['c']:
        to_csv(runs)
    
    web = login_strava(web)
    
    # Strava upload
    count = 0
    for i in runs:
        t1 = time.time()
        time.sleep(1)
        add_strava_entry(i, web)
        curr_date = i['date']
        
        count += 1
        t2 = time.time()
        progress = f'| Added activity on {curr_date} to Strava | Total = {count} of {len(runs)}'
        printProgressBar(count, len(runs), decimals=2, suffix = progress, t1= t1, t2 = t2)
        
    web.driver.close()
    print(f'\nSuccessfully added {count} activities to Strava!')
    return
    
if __name__ == '__main__':
    main()    
