#!/usr/bin/env python
import boto.utils, boto.ec2, datetime
import logging
from datetime import timedelta
from botocreds import aws_access_key_id, aws_secret_access_key

tag_id = "BU-F"
target_region = "ap-southeast-2"


ec2_conn = boto.ec2.connect_to_region(target_region, 
                                      aws_access_key_id=aws_access_key_id, 
                                      aws_secret_access_key=aws_secret_access_key)

volumes = ec2_conn.get_all_volumes()

for volume in volumes:
    butime = int(volume.tags.get(tag_id, 0))
    if butime:
        snaps = volume.snapshots()
        latest_snap_time = None
        for snap in snaps:
            current_snap_time = datetime.datetime.strptime(snap.start_time, boto.utils.ISO8601_MS)
            if latest_snap_time <> None:
                if current_snap_time > latest_snap_time:
                    latest_snap_time = current_snap_time
            else:
                latest_snap_time = current_snap_time
        
        if snaps:
            snap_due = latest_snap_time + timedelta(hours=butime)
            due_now = snap_due < datetime.datetime.utcnow()
        else:
            #Force snapshot if none exists for this volume.
            due_now = True
        if due_now:
            logging.info("Snapping... " + str(volume.id))
            volume.create_snapshot('Auto Snapshot Backup')
        else:
            logging.debug(str(volume.id) + " not due to snap.")
            



            
