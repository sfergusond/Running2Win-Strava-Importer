# Running2Win-Strava Importer
Automatically imports running2win activity data, including descriptions and comments, into Strava or downloads to a CSV file.

# Instructions for Mac

### 1) Download the code
[Click here to download the zip folder with the program files](https://github.com/sfergusond/Running2Win-Strava-Importer/archive/master.zip)

### 2) Extract files into separate folder
Double click on `Running2Win-Strava-Importer-master.zip` to extract all the files into their own folder. The folder should contain the following files:
![step1](https://github.com/sfergusond/imgdump/blob/master/step1.png?raw=true)

### 3) Install Python
Click the link to the right to install Python (if you already have it, it must be at least Python3.7) ([Mac installer](https://www.python.org/ftp/python/3.8.3/python-3.8.3rc1-macosx10.9.pkg)). Then, run the installer. __While you're at this step, download Chrome on your computer if you haven't already, it is required for the program to work__

### 3) Run R2WImporter.py
Right click on R2WImporter.py in folder from step 2. Choose "Open With..." > "Python Launcher". A bunch of stuff will download.

_If any errors occur at this point, follow the Windows instructions below from step 4._

### 4) Enter login info and date filters
After you see "Starting R2W Importer" appear, the program will prompt you to enter your Running2Win login info, two dates, an upload (to Strava) or download (to a .csv file) option, your Strava login method (Google, Facebook, or direct Email/Password entry), and your Strava login info. 

Type the info into each prompt and hit ENTER on your keyboard. Let the program run. It will take a while (about 20 seconds per activity, you do the math). Avoid logging into your Strava account while the program runs. 

![runtime](https://github.com/sfergusond/imgdump/blob/master/prompts.png?raw=true)

### 5) Let the code run
__Do not close the terminal window while the program runs or hit Command+C in the terminal__, print statements will notify you of the program's progress. Some error statements may print, but if the program keeps running just ignore them.

![sucess](https://github.com/sfergusond/imgdump/blob/master/success.png?raw=true)

### If the program quits unexpectedly or becomes stuck for more than a couple minutes:
1) Close and re-open the terminal window
2) Go to Strava and check the date of the most recent activity that was uploaded
3) Re-run the program by copy/pasting `python R2WImporter.py i` 
4) Make sure you type prompt options exactly as they appear (ex. `google` is valid, `Google` is not, `2019-11-02` is valid, `2019-11-2` is not). Make sure your login info is also correct.

# Instructions for Windows

### 1) Download the code
[Click here to download the zip folder with the program files](https://github.com/sfergusond/Running2Win-Strava-Importer/archive/master.zip)
### 2) Extract files into separate folder
Double click on `Running2Win-Strava-Importer-master.zip` to extract all the files from into their own folder. The folder should contain the following files:

![step1](https://github.com/sfergusond/imgdump/blob/master/step1.png?raw=true)
### 3) Install Python
Install Python (if you already have it, it must be at least Python3.7). ([Windows installer](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe)) Then, run the installer. For Windows, check the "Add Python to PATH" box. __While you're at this step, download Chrome on your computer if you haven't already, it is required for the program to work__

![install](https://github.com/sfergusond/imgdump/blob/master/install.png?raw=true)

### 4) Open a Command Terminal in the folder from step 2
Open a command terminal within the folder you made in step 2. [Click here for intructions for Windows and Mac](https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/). You should see something similar to this:

![step4](https://github.com/sfergusond/imgdump/blob/master/step%203.png?raw=true)
### 5) Run the program
You're ready to import your Running2Win data! Type or copy/paste `python R2WImporter.py` (Mac: `python3 R2WImporter.py`) where the blinking cursor is in the terminal you just opened and hit ENTER (__if CTRL+V does something weird, right-click to paste instead__). A bunch of stuff will begin to download.

![runtime](https://github.com/sfergusond/imgdump/blob/master/run.png?raw=true)
### 6) Enter login info and date filters
After you see `Starting R2W Importer`, the program will prompt you to enter your Running2Win login info, two dates, an upload (to Strava) or download (to a .csv file) option, your Strava login method (Google, Facebook, or direct Email/Password entry), and your Strava login info. 

Type the info into each prompt and hit ENTER on your keyboard. Let the program run. It will take a while (about 20 seconds per activity, you do the math). Avoid logging into your Strava account while the program runs. 

![runtime](https://github.com/sfergusond/imgdump/blob/master/prompts.png?raw=true)
### 7) Let the code run
__Do not close the terminal window while the program runs or hit CTRL+C in the terminal__, print statements will notify you of the program's progress. Some error statements may print, but if the program keeps running just ignore them.

![sucess](https://github.com/sfergusond/imgdump/blob/master/success.png?raw=true)

### If the program quits unexpectedly or becomes stuck for more than a couple minutes:
1) Close and re-open the terminal window
2) Go to Strava and check the date of the most recent activity that was uploaded
3) Re-run the program by copy/pasting `python R2WImporter.py i` 
4) Make sure you type prompt options exactly as they appear (ex. `google` is valid, `Google` is not, `2019-11-02` is valid, `2019-11-2` is not). Make sure your login info is also correct.

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
    - Interval Workout Information
    - Member Comments
* If `csv` is entered in the upload/csv prompt, then all gathered activities will be downloaded to a CSV file in the same directory as the downloaded program.
* If `upload` is entered in the upload/csv prompt, then all gathered activities will be uploaded to Strava

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, or email/password combination. __It does not work with Apple logins__.

__Note: Usernames and passwords are not stored by the program__

In progress: matching activity descriptions/race info/interval info downloaded from Running2Win with existing activities on Strava
