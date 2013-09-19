#!/usr/bin/env python

import logging, datetime
logger = logging.getLogger(__name__)

from AWS_utils import SnapUtils

class PruneSnapshots:
    
    def __init__(self):
        """Set up the AWS object"""
        self.AWS = SnapUtils()

    def get_snaps_past_expiry(self, ref_time=datetime.datetime.utcnow()):
        """generate a list of snapshots that are past expiry"""
        logger.info("Attempting to get Snapshots that are past expiry.")
        all_vols = self.AWS.get_all_vols()
        expired_snaps = []
        for vol in all_vols:
            snaps = self.AWS.get_snaps_for_vol(vol)
            for snap in snaps:
                expiry = snap['expiry']
                if expiry:
                    if expiry < ref_time:
                        expired_snaps.append(snap)
        return expired_snaps
    
    def delete_expired_snapshots(self):
        """Delete snapshots that are past expiry"""
        expired_snaps = self.get_snaps_past_expiry()
        for snap in expired_snaps:
            logger.warning("Deleting Snapshot:" + snap['id'])
            self.AWS.delete_snapshot(snap['id'], dry_run=False)
        return expired_snaps

def main():
    PruneSnap_obj = PruneSnapshots()
    return PruneSnap_obj.delete_expired_snapshots()
    
if __name__ == "__main__":
    main()