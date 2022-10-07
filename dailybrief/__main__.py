import sys
import logging
import argparse
import time
from datetime import date
from datetime import datetime
import json

from dailybrief.dailybrief import DailyBrief
from dailybrief.dailybrief import Email


def create_cli() -> argparse.ArgumentParser:
    """Construct the command line interface parser 
    for the script.

    Returns:
        argparse.ArgumentParser: custom command line parser
    """
    parser = argparse.ArgumentParser(
        description="Send a daily briefing email.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--file_credentials",
        type=str,
        default="credentials.json",
        help="full path to json file with credentials",
    )
    parser.add_argument(
        "-d",
        "--file_database",
        type=str,
        default="log.db",
        help="full path to SQLite database file with log information",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="activate verbose logging output",
    )

    return parser


def main() -> int:

    tic = time.time()

    # message information
    runs = [
        "rock creek park north",
        "rock creek park south",
        "washington monument",
        "lincoln memorial",
    ]
    target_date = "2023-07-15"

    parser = create_cli()
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    # read credentials
    cred = json.load(open(args.file_credentials))
    sender = cred.get("sender")
    receiver = cred.get("receiver")
    password = cred.get("password")

    # construct message
    briefer = DailyBrief(args.file_database)
    briefer.set_seed_by_date(seed_date=date.today())
    run = briefer.get_run(runs=runs)
    countdown = briefer.get_countdown(target_date=target_date)
    body = briefer.get_message(run=run, countdown=countdown)

    logging.info(f"Sending message...")

    email = Email(
        sender=sender,
        receiver=receiver,
        subject=f'Daily Briefing | {format(date.today(), "%Y-%m-%d")}',
        body=body,
        run=run,
        countdown=countdown,
    )

    sent_status = briefer.send_email(email, password=password)

    if sent_status:
        logging.info("Delivery successful!")
    else:
        logging.info("Delivery failed.")

    logging.info(f"Runtime: {round(time.time() - tic)} s")

    briefer.clean_up()
    return 0


if __name__ == "__main__":
    sys.exit(main())
