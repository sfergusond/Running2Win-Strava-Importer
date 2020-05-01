# Running2Win-to-Strava-Importer
Automatically imports desired running2win activity data, including descriptions and comments, into Strava

[![Run on Repl.it](https://repl.it/badge/github/sfergusond/Running2Win-to-Strava-Importer)](https://repl.it/github/sfergusond/Running2Win-to-Strava-Importer)

1) Click above button
2) Press the green "Run" button on the Repl.it website
3) Once the packages have been installed, type the arguments into the command line (the black window with an orange ">" in the terminal should show a blinking cursor if you click on it). Or, copy the example below into the command line. Make sure to replace everything inside the double quotes (" ") with your information and desired start/end dates.
4) Let the program run. It will take a while.

# Usage

```
usage: R2Wbot.py \[-h] -ru r2w_username -rp r2w_password -a after_date -b
                 before_date -su strava_email -sp strava_password

Retrieve R2W data and upload to Strava --- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru "myr2wusername" ---

required arguments:
  -ru r2w_username      Running2Win username
  -rp r2w_password      Running2Win password
  -a after_date         Date after which to search for activities on
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -b before_date        Date at which to stop collecting activities form
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -su strava_email      Strava username (MUST BE A GOOGLE EMAIL ADDRESS LINKED TO YOUR STRAVA ACCOUNT)
  -sp strava_password   Strava password 

optional arguments:
  -h, --help            show this help message and exit
```

# Example

```
python R2WBot.py -ru "runner1" -rp "password1" -a "2016-05-31" -b "2020-04-01" -su "stravarunner1" -sp "password2"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The activities will then be uploaded automatically to Strava. 

Note: this will take along time to run, so it is best to keep your machine on until the upload is complete
