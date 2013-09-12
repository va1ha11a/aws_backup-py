#!/usr/bin/env python
""""Backup policy processor. Definitions for backups policies or how to generated 
them should be stored here
results for each time period should give a tuple with the first item being how
often to take the snapshot and a second item for how many of them to keep.
for example "hourly":(1,24) would take a snapshot every 1 hour and keep 24 of 
them before pruning.
"""

import logging
logger = logging.getLogger(__name__)

defined = {
           "STD":{"hourly":(1,24),
                   "daily":(1,31),
                   "weekly":(1,12),
                   "monthly":(1,12),
                   "yearly":(1,7),
                   },
           
           }

def defined_policy(policy_name):
    """Get policy details for defined policies"""
    logger.debug("Getting policy details for policy: " + policy_name)
    try:
        return defined[policy_name]
    except:
        logger.warning("Policy details not found for policy: " + policy_name)
        return None
    