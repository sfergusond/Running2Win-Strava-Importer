# Running2Win-Strava Importer
Automatically imports running2win activity data, including descriptions and comments, into Strava or downloads to a CSV file.

# Instructions

1. [Click here to download the a zip folder with the program files](https://github.com/sfergusond/Running2Win-Strava-Importer/archive/master.zip)

2. Extract all the files from `Running2Win-Strava-Importer-master.zip` into their own folder. The folder should look like this, note the folder path at the top:

![step1](https://github.com/sfergusond/imgdump/blob/master/step1.png?raw=true)

3. Make sure you have Python downloaded and installed ([Windows installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe) | [Mac installer](https://www.python.org/ftp/python/3.8.3/python-3.8.3rc1-macosx10.9.pkg)). Then, run the installer. Check the "Add Python to PATH" box if it exists. __While you're at this step, download Chrome on your computer if you haven't already, it is required for the program to work__

![install](https://github.com/sfergusond/imgdump/blob/master/install.png?raw=true)

4. Open a command terminal within the folder made in step 2. [Click here for intructions for Windows and Mac](https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/). You should see something similar to this:

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
_(If you get some kind of error, then you didn't install Python3.7 correctly. Uninstall Python and try again from step 3)_

6. Next, copy ```pip install -r requirements.txt``` into the command line and hit ENTER on your keyboard. A bunch of stuff will download.

![step6](https://github.com/sfergusond/imgdump/blob/master/step6.png?raw=true)

If that didn't work, try using this command instead: `python -m pip install -r requirements.txt` _(If you still get an error, it's because your terminal isn't aligned to the folder with the downloaded program. See step 4.)_

7. You're ready to run the importer! Type or copy/paste `python R2WImporter.py` into the terminal and hit ENTER. The program will prompt you to enter your Running2Win login info, two dates, an upload (to Strava) or download (to a .csv file) option, your Strava login method (Google, Facebook, or direct Email/Password entry), and your Strava login info. Type the info into each prompt and hit ENTER on your keyboard.

![runtime](https://github.com/sfergusond/imgdump/blob/master/last%20step.png?raw=true)

8. Hit ENTER on your keyboard and let the program run. It will take a while (about 20 seconds per activity, you do the math). Avoid logging into your Strava account while the program runs. __Do not close the terminal window while the program runs or hit CTRL+C or Command+C in the terminal__, print statements will notify you of the program's progress.

9. If for some reason the program is interrupted, go to Strava and check the date of the most recent activity that was uploaded. Then re-run the program. If the program seems to be stuck for more than a minute or two, or if the program quits unexpectedly, you probably entered invalid or misformatted information into the prompts. Close and re-open the terminal window and start again from step 7.

Successful output is shown below. Some error statements may print, but if the program keeps running just ignore them.

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
