# Running2Win-to-Strava-Importer
Automatically imports desired running2win activity data, including descriptions and comments, into Strava

<li> d<li>
1) Download this repository (green button in the upper right, choose ZIP option)
2) Unzip the repository into its own folder on your computer.
3) Make sure you have Python3 downloaded and installed: see https://www.python.org/downloads/ (make sure you download the installer executable, then run the installer once it finishes downloading. Don't try to download the Python file directly)
4) Open a command terminal within the folder you unzipped the repository files (Windows and Mac: https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/)
5) Install pip. First, copy the following into the command terminal you just opened and hit ENTER on your keyboard:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
Then, copy the following and hit ENTER again:
```
python get-pip.py
```
6) Copy ```pip install -r requirements.txt``` into the command line and hit ENTER on your keyboard
7) Once the packages have been installed, type desired arguments into the command line. Alternatively, copy an example from below into the command line. Make sure to replace everything inside the double quotes (" "), but keep the double quotes, with your information and desired start/end dates.
8) Hit ENTER on your keyboard and let the program run. It will take a while. Avoid logging into your Strava account while the program runs.
9) Strava.com may timeout before all of your activities are loaded. If so, check the date of the most recent activity that was uploaded and run the program again (from step 7) with a new start date (change the ```-a``` flag).

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, or email/password combination. It does not work with Apple logins. Make sure the login method flag is set appropriately.

Note: Usernames and passwords are not stored by the program

# Usage

```
usage: R2Wbot.py \[-h] -ru r2w_username -rp r2w_password -a after_date -b
                 before_date -su strava_email -sp strava_password

Retrieve R2W data and upload to Strava --- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru "myr2wusername" ---

required arguments:
  -ru r2w_username      Running2Win username
  -rp r2w_password      Running2Win password
  -a after_date         Date of first activity to import from Running2Win 
                        MUST BE IN FORMAT: YYYY-MM-DD
  -b before_date        Date of last activity to import from Running2Win
                        MUST BE IN FORMAT: YYYY-MM-DD
  -su strava_email      Username/email for Strava/Google/Facebook account, 
                        depending on the value of the -m flag (see below)
  -sp strava_password   Password for Strava/Google/Facebook account, 
                        depending on the value of the -m flag (see below)

optional arguments:
  -h, --help            show this help message and exit
  -m Strava_login_method
                        Method for logging into Strava, default is Google sign-in
                        Default: "Google" (if you do not include this argument, 
                        it will default to Google sign-in)
                        Options: "Email" login to Strava via direct email/password combination
                                 "Facebook" login to Strava using Facebook
                                 "Google" login to Strava using Google
  -c upload/download type 
                        Default: "upload" (if you do not include this argument, activities will be uploaded to Strava)
                        Options: "upload" to upload all activity data to Strava 
                                 "csv" to import data to a local csv file (no upload)
```

# Examples

```
python R2WBot.py -ru "r2wusername" -rp "r2wpassword" -a "2016-05-31" -b "2020-04-01" -su "stravausername1" -sp "stravapassword"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The activities will then be uploaded automatically to Strava. 

```
python R2WBot.py -ru "r2wusername" -rp "r2wpassword" -a "2016-05-31" -b "2020-04-01" -su "stravausername1" -sp "stravapassword" -m "Email"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). Rather than attempting a Google sign-in, the bot will directly enter the given Strava user's email and password into the fields on www.strava.com/login.

```
python R2WBot.py -ru "r2wusername" -rp "r2wpassword" -a "2016-05-31" -b "2020-04-01" -su "stravausername1" -sp "stravapassword" -c "csv"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The activities will be downloaded to a file named "activities.csv" in the same directory as the code. The program will not attempt to login or upload to Strava.

Note: this will take a long time to run, so it is best to keep your machine on until the upload is complete

# Features

Gathers all activity data from Running2Win (not including acticities marked "NO RUN - OFF", "Other", or "Cross Training/Other"), for each activitiy retrieving its activity type, title, distance, time, description, member comments, race information, and interval information.

Uploads each gathered activity from r2w onto your Strava account. Or, downloads to a CSV file if ```-c "csv"``` is passed as an argument.

In progress: matching Running2Win activity descriptions/race info/interval info/comments to existing Strava activity descriptions rather than creating new activities.
