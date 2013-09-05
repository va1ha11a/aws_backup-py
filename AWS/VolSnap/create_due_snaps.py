#!/usr/bin/env python

from AWS_utils import AWSUtils
from policy import defined_policy

class DueSnapshots:
    
    def __init__(self):
        self.AWS = AWSUtils()
    
    def _get_vol_list(self):
        return self.AWS.get_vols_for_backup()
        
    def select_due(self):
        vols = self._get_vol_list()
        for vol in vols:
            policy_details = defined_policy(vol["policy"])
            print policy_details


if __name__ == "__main__":
    x = DueSnapshots()
    x.select_due()
