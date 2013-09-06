#!/usr/bin/env python

from AWS_utils import AWSUtils
from utils import isDueHours, isDueDays, isDueWeeks, isDueMonths, isDueYears
from policy import defined_policy

class BackupSnapshots:
    
    _due_lookup = {"hourly":isDueHours,
                   "daily":isDueDays,
                   "weekly":isDueWeeks,
                   "monthly":isDueMonths,
                   "yearly":isDueYears,
                   }
    
    def __init__(self):
        self.AWS = AWSUtils()
    
    def _get_vol_list(self):
        return self.AWS.get_vols_for_backup()
        
    def select_due(self):
        due_vols = {}
        vols = self._get_vol_list()
        for vol in vols:
            policy_details = defined_policy(vol["policy"])
            due = self._check_vol_snaps(vol, policy_details)
            any_due = bool([bu for bu, isdue in due.iteritems() if isdue])
            if any_due:
                due_vols[vol['id']] = due
        return due_vols
 
    def _choose_snaps(self, snapshots, bu_key):
        return [snap for snap in snapshots if snap['bu-keys'][bu_key]]
            
    def _check_vol_snaps(self, volume, policy):
        snaps =  self.AWS.get_snaps_for_vol(volume["id"])
        due_list = {bu_level:due_func(self._choose_snaps(snaps, bu_level), policy[bu_level][0]) for bu_level, due_func in self._due_lookup.iteritems()}
        return due_list
        
if __name__ == "__main__":
    x = BackupSnapshots()
    print x.select_due()
