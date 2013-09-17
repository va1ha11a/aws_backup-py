"""Some definitions of reports that could be sent via email."""

import datetime
from AWS_utils import SnapUtils
from prune_old_snaps import PruneSnapshots

snap_obj = SnapUtils()

def expires_future(future_datetime_utc):
    """Get snaps due to expire by a future date"""
    obj = PruneSnapshots()
    snaps = obj.get_snaps_past_expiry(future_datetime_utc)
    return snaps

def _get_latest(volume_id):
    """get latest snapshot for a volume"""
    all_snaps =  snap_obj.get_snaps_for_vol(volume_id)
    latest = datetime.datetime(1900,1,1)
    for snap in all_snaps:
        if snap['start_time'] > latest:
            latest = snap['start_time']
    if latest != datetime.datetime(1900,1,1):
        return latest
    else:
        return None

def latest_snap_all_vols():
    vol_latest = {}
    vols = snap_obj.get_all_vols()
    for vol in vols:
        vol_latest[vol] = _get_latest(vol)
    return vol_latest

if __name__ == "__main__":
    print latest_snap_all_vols()
    