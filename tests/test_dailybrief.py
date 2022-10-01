"""
Description: unit tests for the dailybrief class.
Author: Haley Hunter-Zinck
Date: 2022-10-01
"""

from datetime import date

from dailybrief.dailybrief import DailyBrief



briefer = DailyBrief()

def test_set_seed_by_date():
    seed_yesterday = briefer.set_seed_by_date(date(2022, 9, 30))
    seed_today = briefer.set_seed_by_date(date(2022, 10, 1))
    assert seed_yesterday != seed_today
