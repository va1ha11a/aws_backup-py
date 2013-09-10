#!/usr/bin/env python

from AWS_utils import SnapUtils
from utils import isDueHours, isDueDays, isDueWeeks, isDueMonths, isDueYears
from policy import defined_policy

class BackupSnapshots:
    """Select snapshots that are due and create them.
    Tag them to match the due snapshot types."""
    
    """Map isDue check functions to the keys"""
    _due_lookup = {"hourly":isDueHours,
                   "daily":isDueDays,
                   "weekly":isDueWeeks,
                   "monthly":isDueMonths,
                   "yearly":isDueYears,
                   }
    
    def __init__(self):
        """Set up the AWS object"""
        self.AWS = SnapUtils()
        
    def select_due(self):
        """Generate a list of volumes with snapshots due.
        Includes dict with what snapshots are due"""
        due_vols = {}
        vols = self.AWS.get_vols_for_backup()
        for vol in vols:
            policy_details = defined_policy(vol["policy"])
            if policy_details == None:
                continue
            due = self._check_vol_snaps(vol, policy_details)
            any_due = bool([bu for bu, isdue in due.iteritems() if isdue])
            if any_due:
                due_vols[vol['id']] = due
        return due_vols

    def create_due_snapshots(self):
        """Create due snapshots and tag appropriatly."""
        new_snaps = []
        due_vols = self.select_due()
        for volume, due in due_vols.iteritems():
            snap_id = self.AWS.create_snap_for_vol(volume, due)
            new_snaps.append(snap_id)
        return new_snaps
        
 
    def _choose_snaps(self, snapshots, bu_key):
        """Filter snapshots by backup key. This allows for checking by key
        i.e. only could other monthly snapshots when checking for monthly snaps due."""
        return [snap for snap in snapshots if snap['bu-keys'][bu_key]]
            
    def _check_vol_snaps(self, volume, policy):
        """Check a specific volume for due snapshots agains the specified backup policy"""
        snaps =  self.AWS.get_snaps_for_vol(volume["id"])
        due_list = {bu_level:due_func(self._choose_snaps(snaps, bu_level), policy[bu_level][0]) for bu_level, due_func in self._due_lookup.iteritems()}
        return due_list
        
if __name__ == "__main__":
    x = BackupSnapshots()
    print x.create_due_snapshots()
