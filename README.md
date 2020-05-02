# Running2Win-to-Strava-Importer
Automatically imports desired running2win activity data, including descriptions and comments, into Strava

# Instructions

1. [Click here to download the program](https://github.com/sfergusond/Running2Win-to-Strava-Importer/archive/master.zip)

2. Unzip the downloaded zip file into its own folder on your computer. The folder with the unzipped files should look like this, note the folder path at the top:

![step1](https://github.com/sfergusond/imgdump/blob/master/step1.png?raw=true)

3. Make sure you have Python3 downloaded and installed: see https://www.python.org/downloads/ (*make sure you download the installer executable, then run the installer once it finishes downloading. __Don't try to download the Python file directly__*) __Also, make sure you have Chrome downloaded on your computer__

4. Open a command terminal within the folder you unzipped the repository files. [Click here for intructions for Windows and Mac](https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/). You should see something similar to this:

![step4](https://github.com/sfergusond/imgdump/blob/master/step%203.png?raw=true)

5. Install pip. First, copy/paste the following into the command terminal (__if CTRL+V does something weird, right-click to paste instead__) you just opened and hit ENTER on your keyboard: 
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
Then, copy the following and hit ENTER again:   
```
python get-pip.py
```

After completing both, your terminal should resemble something like this:

![step5](https://github.com/sfergusond/imgdump/blob/master/step5.png?raw=true)

6. Next, copy ```pip install -r requirements.txt``` into the command line and hit ENTER on your keyboard:

![step6](https://github.com/sfergusond/imgdump/blob/master/step6.png?raw=true)

7. Copy an example from below into the command line. Option 1 is most likely what you want to use. If you don't use Google to login to Strava, use Option 2 with either `-m "Email"` or `-m "Facebook"` depending on how you login to Strava. __Make sure to replace everything inside double quotes (" "), but keep the double quotes, with your information and desired start/end dates.__ You likely need to use your LEFT and RIGHT arrow keys to navigate the cursor through the input once you paste it into your command terminal, mouse clicks may not work.

_Option 1:_
```
python R2WBot.py -ru "r2wusername" -rp "r2wpassword" -a "2016-05-31" -b "2020-04-01" -su "stravausername1" -sp "stravapassword"
```
In your terminal, it would look like this:

![step7](https://github.com/sfergusond/imgdump/blob/master/last%20step.png?raw=true)

_Option 2:_
```
python R2WBot.py -ru "r2wusername" -rp "r2wpassword" -a "2016-05-31" -b "2020-04-01" -su "stravausername1" -sp "stravapassword" -m "Email"
```

8. Hit ENTER on your keyboard and let the program run. It will take a while (about 20 seconds per activity, you do the math). Avoid logging into your Strava account while the program runs. __Do not close the terminal window while the program runs__, print statements will notify you of the program's progress.

9. If for some reason the program is interrupted, go to Strava and check the date of the most recent activity that was uploaded. Then, run the program again from step 7 with a new start date (change the ```-a``` flag). _You can use the UP or DOWN arrow keys to load previously run commands into the current command prompt instead of retyping everything_ The image belows displays the output if the program is running sucessfully. The gathered statements show the progress of downloading activities from Running2Win while the Added to Strava statements show the progress of uploading your activities to Strava.

![sucess](https://github.com/sfergusond/imgdump/blob/master/success.png?raw=true)

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, or email/password combination. __It does not work with Apple logins__. Make sure the login method flag is set appropriately.

__Note: Usernames and passwords are not stored by the program__

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
