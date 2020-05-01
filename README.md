# Running2Win-to-Strava-Importer
Automatically imports desired running2win activity data, including descriptions and comments, into Strava

[![Run on Repl.it](https://repl.it/badge/github/sfergusond/Running2Win-to-Strava-Importer)](https://repl.it/github/sfergusond/Running2Win-to-Strava-Importer)

# Usage

usage: R2Wbot.py \[-h] -ru r2w_username -rp r2w_password -a after_date -b
                 before_date -su strava_email MUST BE A GOOGLE EMAIL ADDRESS
                 LINKED TO YOUR STRAVA ACCOUNT -sp strava_password

Retrieve R2W data and upload to Strava [PUT ALL ARGUMENTS IN DOUBLE QUOTES |
ex: -ru "myr2wusername"]

optional arguments:
  -h, --help            show this help message and exit
  -ru r2w_username      Running2Win username
  -rp r2w_password      Running2Win password
  -a after_date         Date after which to search for activities on
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -b before_date        Date at which to stop collecting activities form
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -su strava_email      Strava username (MUST BE A GOOGLE EMAIL ADDRESS LINKED TO YOUR STRAVA ACCOUNT)
  -sp strava_password   Strava password
