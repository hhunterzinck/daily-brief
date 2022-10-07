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
    def __init__(
        self,
        sender: str,
        receiver: str,
        body: str,
        subject: str = "Daily Briefing",
        sent_datetime: str = None,
        sent_status: bool = None,
        run: str = None,
        countdown: int = None,
    ):
        self.sent_datetime = sent_datetime
        self.sent_status = sent_status
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.run = run
        self.countdown = countdown

    def set_sent_status(self, sent_status: bool):
        """Set the sent instance variable

        Args:
            sent (bool): True if sent and False otherwise
        """
        self.sent_status = sent_status

    def set_sent_datetime(self, sent_datetime: str):
        """Set the sent timestamp.

        Args:
            sent_datetime (str): _description_
        """
        self.sent_datetime = sent_datetime


class DailyBrief:
    def __init__(self, file: str = None):
        if file is not None:
            self.conn = self.initialize_database(file=file)
        else:
            self.conn = None

    def format_text(self, text: str) -> str:
        """Format text for insertion into the sqlite database

        Args:
            text (str): text to insert

        Returns:
            str: formatted text
        """
        if text is None:
            return ""

        if not isinstance(text, str):
            text = str(text)
        return text.replace("'", "''")

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

        query = f"""INSERT INTO log (sent_datetime, sent_status, sender, receiver, subject, body, run, countdown)
                    VALUES('{self.format_text(email.sent_datetime)}', 
                            '{self.format_text(email.sent_status)}', 
                            '{self.format_text(email.sender)}', 
                            '{self.format_text(email.receiver)}', 
                            '{self.format_text(email.subject)}', 
                            '{self.format_text(email.body)}', 
                            '{self.format_text(email.run)}', 
                            {email.countdown});"""
        logging.info(f"executing query: {query}")

        cur = self.conn.cursor()
        try:
            cur.execute(query)
            self.conn.commit()
            status = True
        except Exception as e:
            logging.error(f"Error in insertion into log {e}")
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

    def get_last_run(self) -> str:
        """Get the last recorded run in the log.

        Returns:
            str: last run or None if nothing in the log
        """
        statement = f"SELECT run FROM log ORDER BY rowid DESC LIMIT 1"
        cur = self.conn.cursor()
        cur.execute(statement)
        result = cur.fetchall()
        cur.close()
        if len(result):
            return result[0][0]
        return None

    def get_run(self, runs: list, exclude_last_run: bool = True) -> str:
        """Select a run at random, removing the last recorded run
        if requested.

        Args:
            runs (list): list of runs from which to sample

        Returns:
            str: randomly selected run
        """
        if exclude_last_run:
            last_run = self.get_last_run()
            if last_run is not None:
                runs.remove(last_run)
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

    def get_message(self, run: str, countdown: int) -> str:
        msg_run = f"Today's run: '{run}'"
        msg_countdown = f"Days until move-out: {countdown}"
        return f"{msg_run}\n{msg_countdown}"

    def send_email(self, email: Email, password: str) -> bool:
        sent_status = False

        message = f"Subject: {email.subject}\n\n{email.body}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        try:
            server.starttls()
            server.login(email.sender, password)
            server.sendmail(email.sender, email.receiver, message)
            sent_status = True

            email.set_sent_status(sent_status)
            email.set_sent_datetime(format(datetime.now(), "%Y-%m-%d %H:%M:%S"))
            self.update_database_log(email=email)
        except Exception as e:
            logging.error(e)
        finally:
            server.quit()

        return sent_status
