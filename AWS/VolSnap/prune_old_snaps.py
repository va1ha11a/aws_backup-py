#!/usr/bin/env python

import logging
logger = logging.getLogger(__name__)

from AWS_utils import SnapUtils

class PruneSnapshots:
    
    def __init__(self):
        """Set up the AWS object"""
        self.AWS = SnapUtils()
           
    def _choose_snaps(self, snapshots, bu_key):
        """Filter snapshots by backup key. This allows for checking by key
        i.e. only could other monthly snapshots when checking for monthly snaps due."""
        return [snap for snap in snapshots if snap['bu-keys'][bu_key]]
    
if __name__ == "__main__":
    pass