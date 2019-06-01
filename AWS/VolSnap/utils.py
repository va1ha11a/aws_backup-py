#!/usr/bin/env python

import logging
logger = logging.getLogger(__name__)

import datetime
import settings
from dateutil.relativedelta import relativedelta

res = datetime.timedelta(minutes=settings.due_resolution_mins)


def generate_expiry_date(bu_keys, created_date=datetime.datetime.utcnow()):
    """Generate and expiry date for a snapshot based on its created date 
    and the policy details of the policy it is in"""
    timeframe_map = {
        "hourly": "hours",
        "daily": "days",
        "weekly": "weeks",
        "monthly": "months",
        "yearly": "years",
    }
    furthest_date = created_date
    for timeframe, value in bu_keys.iteritems():
        if value:
            count = bu_keys[timeframe][0] * bu_keys[timeframe][1]
            test_date = created_date + relativedelta(
                **{timeframe_map[timeframe]: count})
            if furthest_date < test_date:
                furthest_date = test_date
    return furthest_date


def _ckeckDue(times, time_delta, ref_time):
    """Generic due checker based on a ref time and time delta"""
    logging.debug("Checking due time")
    logging.debug("due times: " + str(times))
    logging.debug("time delta: " + str(time_delta))
    logging.debug("Reference time: " + str(ref_time))
    if not ref_time:
        ref_time = datetime.datetime.utcnow()
    #Get all snaps since time_delta before ref_time
    last = next((snap for snap in times
                 if snap["start_time"] > (ref_time + res) - time_delta), None)
    # if there are none then snap is due.
    if last:
        return False
    else:
        return True


def isDueHours(times, hours=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = datetime.timedelta(hours=hours)
    return _ckeckDue(times, time_delta, ref_time)


def isDueDays(times, days=1, ref_time=None):
    """Return if a daily snapshot is due based on if any daily snapshots fall within the given hours (24/day)"""
    time_delta = datetime.timedelta(hours=days * 24)
    return _ckeckDue(times, time_delta, ref_time)


def isDueWeeks(times, weeks=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = datetime.timedelta(days=weeks * 7)
    return _ckeckDue(times, time_delta, ref_time)


def isDueMonths(times, months=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = relativedelta(months=months)
    return _ckeckDue(times, time_delta, ref_time)


def isDueYears(times, years=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = relativedelta(years=years)
    return _ckeckDue(times, time_delta, ref_time)


due_lookup_function_map = {
    "hourly": isDueHours,
    "daily": isDueDays,
    "weekly": isDueWeeks,
    "monthly": isDueMonths,
    "yearly": isDueYears,
}
