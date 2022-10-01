"""
Description: send a daily email.
Author: Haley Hunter-Zinck
Date: 2022-09-18
"""

import smtplib
import logging
import random
from datetime import date, datetime
import sqlite3
import os.path

class Email:
    def __init__(self, send_datetime: str, sent_status: bool, sender: str, receiver: str,
                        body: str, run: str, countdown: str, subject: str="Daily Briefing"):
        self.send_datetime=send_datetime
        self.sent_status=sent_status
        self.sender=sender
        self.receiver=receiver
        self.subject=subject
        self.body=body
        self.run=run
        self.countdown=countdown


class DailyBrief:

    def __init__(self, file: str):
        self.conn = self.initialize_database(file=file)

    def initialize_database(self, file: str) -> sqlite3.Connection:
        """Initialize the database, if it doesn't already exist.

        Args:
            file (str): full path to sqlite database file

        Returns:
            sqlite3.Connection: database connection object
        """
        db_exists = os.path.exists(file)
        conn = sqlite3.connect(file)

        if not db_exists:
            cur = conn.cursor()
            query = """CREATE TABLE log (
                        log_id INTEGER PRIMARY KEY ASC,
                        sent_datetime TEXT,
                        sent_status INTEGER,
                        sender TEXT,
                        receiver TEXT,
                        subject TEXT,
                        body TEXT,
                        run TEXT,
                        countdown INTEGER
                    )"""
            cur.execute(query)
            cur.close()
        
        return conn

    def update_database_log(self, email: Email) -> bool:
        status = False

        query = f"""INSERT INTO log 
                    (sent_datetime, 
                        sent_status, 
                        sender, 
                        receiver, 
                        subject, 
                        body, 
                        run, 
                        countdown)
                    VALUES
                    ({email.sent_datetime}, 
                        {email.sent_status}, 
                        {email.sender}, 
                        {email.receiver}, 
                        {email.subject}, 
                        {email.body}, 
                        {email.run}, 
                        {email.countdown})
                )"""

        cur = self.conn.cursor()
        try:
            cur.execute(query)
            self.conn.commit()
            status = True
        except Exception as e:
            logging.error(e)
        finally:
            cur.close()
        return status

    def clean_up(self) -> bool:
        """Close the database connection.

        Returns:
            bool: True if database connection successfully closed.
        """
        status = False
        try:
            self.conn.close()
            status = True
        except Exception as e:
            logging.error(e)

        return status
    

    def set_seed_by_date(self, seed_date: date) -> int:
        """Set the random seed using a provided date.

        Args:
            seed_date (date): date to use for seed

        Returns:
            int: seed used
        """
        seed = int(seed_date.strftime("%Y%m%d"))
        random.seed(seed)
        return seed

    def get_run(self, runs: list) -> str:
        """Select a run at random.

        Args:
            runs (list): list of runs from which to sample

        Returns:
            str: randomly selected run
        """
        return random.sample(runs, k=1)[0]

    def get_countdown(self, target_date: str) -> int:
        """Calculate a countdown between today's date and a target date.
        If the target date is today's date, will return 0.

        Args:
            target_date (str): target date for which to calculate the 
                countdown.

        Returns:
            int: number of days between the target date and today.
        """
        datetime_today = datetime.today().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        delta = datetime.strptime(target_date, "%Y-%m-%d") - datetime_today
        return delta.days

    def get_message_run(self, runs: list) -> str:
        """Construct daily run mesage by randomly 
        sampling one run from a list.

        Args:
            runs (list): labels for potential running routes

        Returns:
            str: daily run message
        """
        msg = f"Today's run: '{self.get_run(runs=runs)}'"
        return msg

    def get_message_countdown(self, target_date: str) -> str:
        """Construct a message that displays calculating
        number of ideas from today to a target date

        Args:
            target_date (str): target date for which to calculate countdown

        Returns:
            str: countdown message
        """
        msg = f"Days until move-out: {self.get_countdown(target_date=target_date)}"
        return msg

    def send_email(self, email: Email, password: str) -> bool:
        sent = False

        message = f"Subject: {email.subject}\n\n{email.body}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        try:
            server.starttls()
            server.login(email.sender, password)
            server.sendmail(email.sender, email.receiver, message)
            sent = True
        except Exception as e:
            logging.error(e)
        finally:
            server.quit()

        return sent
