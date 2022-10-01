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
usage: dailybrief [-h] [-c FILE_CREDENTIALS] [-v]

Send a daily briefing email.

optional arguments:
  -h, --help            show this help message and exit
  -c FILE_CREDENTIALS, --file_credentials FILE_CREDENTIALS
                        full path to json file with credentials (default:
                        credentials.json)
  -v, --verbose         activate verbose logging output (default: False)
```

An example command:

```
dailybrief -c /path/to/my/credentials.json -v
```

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