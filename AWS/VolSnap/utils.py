#!/usr/bin/env python
import datetime
from dateutil.relativedelta import relativedelta

def _ckeckDue(times, time_delta, ref_time):
    """Generic due checker based on a ref time and time delta"""
    if not ref_time:
        ref_time = datetime.datetime.now()
    #Get all snaps since time_delta before ref_time
    last = next((snap for snap in times if snap[0] > ref_time - time_delta), None)
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
    time_delta = datetime.timedelta(hours=days*24)
    return _ckeckDue(times, time_delta, ref_time)

def isDueWeeks(times, weeks=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = datetime.timedelta(days=weeks*7)
    return _ckeckDue(times, time_delta, ref_time)

def isDueMonths(times, months=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = relativedelta(months=months)
    return _ckeckDue(times, time_delta, ref_time)

def isDueYears(times, years=1, ref_time=None):
    """Return if an hourly snapshot is due based on if any hourly snapshots fall within the given hour"""
    time_delta = relativedelta(years=years)
    return _ckeckDue(times, time_delta, ref_time)

