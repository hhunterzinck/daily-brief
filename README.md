# Daily Brief
This tool sends a daily breifing email.  The email can be automated through a cron job.  

## Installation

After cloning the repository to your machine, navigate to the directory and run

```
pip install -r requirements.txt
pip install .
```

## Usage

To see usage, run

```shell
dailybrief -h
```

which outputs

```
usage: dailybrief [-h] [-c FILE_CREDENTIALS] [-d FILE_DATABASE]
                  [-p FILE_PARAMETERS] [-v]

Send a daily briefing email.

optional arguments:
  -h, --help            show this help message and exit
  -c FILE_CREDENTIALS, --file_credentials FILE_CREDENTIALS
                        full path to json file with credentials (default:
                        credentials.json)
  -d FILE_DATABASE, --file_database FILE_DATABASE
                        full path to SQLite database file with log information
                        (default: log.db)
  -p FILE_PARAMETERS, --file_parameters FILE_PARAMETERS
                        full path JSON file with user defined parameters
                        (default: parameters.json)
  -v, --verbose         activate verbose logging output (default: False)
```

An example command:

```
dailybrief -c /path/to/my/credentials.json -p /path/to/my/parameters.json -v
```

A template for the parameters file is available in the `parameters_template.json`.

## Automation

Automate with a daily cron job.  In the console type

```
crontab -e
```

and paste the following command to send the email every day at 6am local time
```
0 6 * * * /path/to/python /path/to/dailybrief -c /path/to/credentials.json
```

substituting the paths for your files.  