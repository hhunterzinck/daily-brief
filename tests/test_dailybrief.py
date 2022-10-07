"""
Description: unit tests for the dailybrief class.
Author: Haley Hunter-Zinck
Date: 2022-10-01
"""

from datetime import date

from dailybrief.dailybrief import DailyBrief



briefer = DailyBrief()
runs = ['a','b','c','d','e']

def test_set_seed_by_date():
    seed_yesterday = briefer.set_seed_by_date(date(2022, 9, 30))
    seed_today = briefer.set_seed_by_date(date(2022, 10, 1))
    assert seed_yesterday != seed_today

def test_get_run_one():
    run = briefer.get_run(runs=runs, exclude_last_run=False)
    assert len(run) == 1

def test_get_run_sample():
    run = briefer.get_run(runs=runs, exclude_last_run=False)
    assert run in runs
    
def test_get_countdown_zero():
    countdown = briefer.get_countdown(format(date.today(), '%Y-%m-%d'))
    assert countdown == 0