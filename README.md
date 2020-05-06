# Running2Win-Strava Importer
Automatically imports running2win activity data, including descriptions and comments, into Strava or downloads to a CSV file.

# Instructions for Mac

### 1) Download the program
[Click here to download the zip folder with the program files](https://drive.google.com/file/d/11l9bT0uf3kwYhl7FL-KqkdouRBv9GI3c/view?usp=sharing). 

While you're at this step, go to `chrome://settings/help` and make sure you have at least __Chome Version 81__ installed.

### 2) Extract files
Once downloaded, double click on __r2wimporter.zip__ to extract all the files into their own folder (it'll be called __r2wimporter__ even though the screenshot has a different name). 

Drag the folder to the desktop.__ Open the folder, and it should look like this:

![SCREENSHOT1](https://github.com/sfergusond/imgdump/blob/master/s4.png?raw=true)

### 3) Open a terminal window
Open Spotlight search (I think that's what the main search thing is called? idk, I don't use a Mac) and search for __terminal__. Double click the first result.

### 4) A few commands
Copy/paste the following commands, one at a time into the field denoted by the `$` _(press ENTER after entering each line and wait for a new line beginning with_ `$` _to appear again before moving on to the next one)_

1) `cd Desktop/r2wimporter`  _(if that didn't work, [see this quick article about how to open a terminal at a specific folder](https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/). You want to open the terminal in the folder on your desktop called __r2wimporter__)_
2) `python3 --version` _(if that doesn't output a single line with something like_ `Python3.8` _then you need to [download Python3.8](https://www.python.org/ftp/python/3.8.3/python-3.8.3rc1-macosx10.9.pkg). See screenshot below)_

![SCREENSHOT2](https://github.com/sfergusond/imgdump/blob/master/s3.png?raw=true)

3) `python3 -m pip install --upgrade pip` (if that doesn't work, try `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` then `python get-pip.py`)
4) `python3 -m pip install -r requirements.txt`
5) `python3 R2WImporter.py` (this starts the program)

### 5) The program is running
The program will prompt you to enter some information in the same terminal window you opened. It should all be self explanatory, just hit ENTER once after typing each piece of information.

The program will ask you for you Running2Win login info, after which the download will begin. If you chose to upload anything to Strava, the program will prompt you for Strava login info after the Running2Win data is downloaded.

### 6) Let the code run
__Do not close the terminal window while the program runs or hit Control+C in the terminal.__ Print statements will notify you of the program's progress. Some error statements may print, but ignore them if the program keeps running. 

If the program seems stalled for more than a few minutes, just hit ENTER into the terminal window and wait for a minute. Usually this is caused by the web browser running in the background timing out.
  
### If errors occur, the program quits unexpectedly, or hitting ENTER doesn't get the program to continue

You probably have typos in your username/password information:
1) Type __Control+C__ in the terminal window, then type `python3 R2WImporter.py` to restart the program.
2) If the program uploaded anything to Strava, go to Strava and check the date of the most recent activity that was uploaded to avoid making any duplicates.

# Instructions for Windows

### 1) Download the code
[Click here to download the zip folder with the program files](https://drive.google.com/file/d/1g1406XJyo4tJwee1R8f9-rd0ccGOL84U/view?usp=sharing). Double click __R2WImporter.zip__ to extract the files.

While you're at this step, go to chrome://settings/help and make sure you have at least __Chome Version 81__ installed.

### 2) Run the program
Double click on __R2WImporter.exe__ to run the program. _It will take about 5-10 seconds to load once the window pops up._

### 3) The program is running
The program will prompt you to enter some information in the same terminal window you opened. It should all be self explanatory, just hit ENTER once after typing each piece of information.

The program will ask you for you Running2Win login info, after which the download will begin. If you chose to upload anything to Strava, the program will prompt you for Strava login info after the Running2Win data is downloaded.

### 4) Let the code run
__Do not close the terminal window while the program runs or hit CTRL+C in the terminal__, print statements will notify you of the program's progress. Some error statements may print, but if the program keeps running just ignore them. If the program seems stalled for more than a few minutes, just hit ENTER into the terminal window. Usually this is caused by the web browser running in the back ground timing out.
  
### If errors occur, the program quits unexpectedly, or becomes stuck for more than a couple minutes

You probably have typos in your username/password information:
1) Type __CTRL+C__ in the terminal window, then re-run __R2WImporter.exe__.
2) If the program uploaded anything to Strava, go to Strava and check the date of the most recent activity that was uploaded to avoid making any duplicates.

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
    - Max HR
    - Race Information
    - Interval Workout Information
    - Member Comments
* If `csv` is entered in the upload/csv prompt, then all gathered activities will be downloaded to a CSV file in the same directory as the downloaded program.
* If `upload` is entered in the upload/csv prompt, then all gathered activities will be uploaded to Strava
* If comment is entered in the upload/csv prompt, then R2WImporter will attempt to match descriptions from R2W with activities existing on Strava. User specifies how strict the matching policy is and what to do if no match is found (append incoming decscription to an existing Strava activity or create a new activity or ignore). Missing activities from Strava will be automatically uploaded.

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, Apple ID, or email/password combination.

__Note: Usernames and passwords are not stored by the program__
