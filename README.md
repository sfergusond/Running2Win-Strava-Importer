# Running2Win-Strava Importer
Automatically imports running2win activity data, including descriptions and comments, into Strava or downloads to a CSV file.

# Instructions

1. [Click here to download the program](https://github.com/sfergusond/Running2Win-Strava-Importer/archive/master.zip)

2. Unzip the downloaded zip file into its own folder on your computer. The folder with the unzipped files should look like this, note the folder path at the top:

![step1](https://github.com/sfergusond/imgdump/blob/master/step1.png?raw=true)

3. Make sure you have Python3.7 downloaded and installed: see https://www.python.org/downloads/ (*make sure you download the __installer executable__, then run the installer once it finishes downloading. Don't try to download the Python3.7 file directly*) Check the "Add Python3.7 to PATH" box if it exists.) __While you're at this step, donwload Chrome on your computer if you haven't already, it is required for the program to work__

![install](https://github.com/sfergusond/imgdump/blob/master/install.png?raw=true)

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
_(If you get some kind of error, then you didn't install Python3.7 correctly. Uninstall Python and try again from step 3)_
![step5](https://github.com/sfergusond/imgdump/blob/master/step5.png?raw=true)

6. Next, copy ```pip install -r requirements.txt``` into the command line and hit ENTER on your keyboard. A bunch of stuff will download.

![step6](https://github.com/sfergusond/imgdump/blob/master/step6.png?raw=true)

If that didn't work, try using this command instead: `python -m pip install -r requirements.txt` _(If you still get an error, it's because your terminal isn't aligned to the folder with the downloaded program. See step 4.)_

7. You're ready to run the importer! Type or copy/paste `python R2WImporter.py` into the terminal and hit ENTER. The program will prompt you to enter your Running2Win login info, two dates, an upload (to Strava) or download (to a .csv file) option, your Strava login method (Google, Facebook, or direct Email/Password entry), and your Strava login info. Type the info into each prompt and hit ENTER on your keyboard.

8. Hit ENTER on your keyboard and let the program run. It will take a while (about 20 seconds per activity, you do the math). Avoid logging into your Strava account while the program runs. __Do not close the terminal window while the program runs or hit CTRL+C or Command+C in the terminal__, print statements will notify you of the program's progress.

9. If for some reason the program is interrupted, go to Strava and check the date of the most recent activity that was uploaded. Then re-run the program. If the program seems to be stuck for more than a minute or two, or if the program quits unexpectedly, you probably entered invalid or misformatted information into the prompts. Close and re-open the terminal window and start again from step 7.

![sucess](https://github.com/sfergusond/imgdump/blob/master/success.png?raw=true)

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, or email/password combination. __It does not work with Apple logins__.

__Note: Usernames and passwords are not stored by the program__

# Features

* Gathers all activity data from Running2Win, including non-running activities such as Cross Training, NO RUN - OFF, and Other activity types. Activites will be gather beginning from the specified begin date to the specified end date.
* For each activity, the following information is retrieved:
  - Date
  - Distance
  - Time
  - Activity Type
  - Activity Title
  - And, if they exist:
    - Description _(private notes not included)_
    - Difficulty
    - Average HR
    -  Max HR
    - Race Information
    - Interval Information
    - Member Comments
* If `csv` is entered in the upload/csv prompt, then all gathered activities will be downloaded to a CSV file in the same directory as the downloaded program.
* If `upload` is entered in the upload/csv prompt, then all gathered activities will be uploaded to Strava

In progress: matching activity descriptions/race info/interval info downloaded from Running2Win with existing activities on Strava
   
# Advanced Usage

```
usage: R2WImporter.py \[-h] -ru r2w_username -rp r2w_password -a after_date -b
                 before_date [-su strava_email] [-sp strava_password] 
                 [-m strava_login_method] [-c upload/download type]

Retrieve R2W data and upload to Strava --- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru "myr2wusername" ---

required arguments:
  -ru r2w_username      Running2Win username
  -rp r2w_password      Running2Win password
  -a after_date         Date of first activity to import from Running2Win 
                        MUST BE IN FORMAT: YYYY-MM-DD
  -b before_date        Date of last activity to import from Running2Win
                        MUST BE IN FORMAT: YYYY-MM-DD

optional arguments:
  -h, --help            show this help message and exit
  -su strava_email      Username/email for Strava/Google/Facebook account, 
                        depending on the value of the -m flag (see below)
  -sp strava_password   Password for Strava/Google/Facebook account, 
                        depending on the value of the -m flag (see below)
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
python R2WBot.py -ru "r2w_username" -rp "r2w_password" -a "2016-05-31" -b "2020-04-01" -su "strava_username1" -sp "strava_password"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The program will attempt to sign-in to Strava via Google. The activities will then be uploaded automatically to Strava. 

```
python R2WBot.py -ru "r2w_username" -rp "r2w_password" -a "2016-05-31" -b "2020-04-01" -su "strava_username1" -sp "strava_password" -m "Email"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). Rather than attempting a Google sign-in, the bot will directly enter the given Strava user's email and password into the fields on www.strava.com/login. The activities will then be uploaded to Strava.

```
python R2WBot.py -ru "r2w_username" -rp "r2w_password" -a "2016-05-31" -b "2020-04-01" -c "csv"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The activities will be downloaded to a file named "activities.csv" in the same directory as the code. The program will not attempt to login or upload to Strava.
