'''
Description: send a daily email.
Author: Haley Hunter-Zinck
Date: 2022-09-18
'''

import smtplib
import logging
import random
from datetime import date, datetime

from email.message import EmailMessage


class DailyBrief:

    def set_seed_by_date(self, seed_date: date) -> int:
        """Set the random seed using a provided date.

        Args:
            seed_date (date): date to use for seed

        Returns:
            int: seed used
        """
        seed = int(date.today().strftime("%Y%m%d"))
        random.seed(seed)
        return seed

    def get_message_run(self, runs: list) -> str:
        """Construct daily run mesage by randomly 
        sampling one run from a list.

        Args:
            runs (list): labels for potential running routes

        Returns:
            str: daily run message
        """
        msg = f'Today\'s run: \'{random.sample(runs, k=1)[0]}\''
        return msg

    def get_message_countdown(self, target_date: str) -> str:
        """Construct a message that displays calculating
        number of ideas from today to a target date

        Args:
            target_date (str): target date for which to calculate countdown

        Returns:
            str: countdown message
        """
        msg = ''
        delta = datetime.strptime(target_date, '%Y-%m-%d') - datetime.today()
        msg = f'Days until move-out: {delta.days}'
        return msg

    def send_email(self, sender: str, receiver: str, body: str, password: str, subject: str='Daily Briefing') -> bool:
        sent = False

        message = f'Subject: {subject}\n\n{body}'

        server = smtplib.SMTP("smtp.gmail.com", 587)
        try:
            server.starttls() 
            server.login(sender, password)
            server.sendmail(sender, receiver, message)
            sent=True
        except Exception as e:
            logging.error(e)
        finally:
            server.quit()

        return sent
