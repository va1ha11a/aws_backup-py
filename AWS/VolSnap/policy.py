#!/usr/bin/env python
""""Backup policy processor. Definitions for backups policies or how to generated 
them should be stored here"""

defined = {
           "TEST":{"hourly":(1,24),
                   "daily":(1,31),
                   "weekly":(1,12),
                   "monthly":(1,12),
                   "yearly":(1,7),
                   },
           
           }