#!/usr/bin/env python
"""Keep N days of backups."""
import boto.ec2, boto.utils, datetime, logging
from botocreds import aws_access_key_id, aws_secret_access_key

tag_id = "BU-N"
target_region = "ap-southeast-2"


ec2_conn = boto.ec2.connect_to_region(target_region, 
                                      aws_access_key_id=aws_access_key_id, 
                                      aws_secret_access_key=aws_secret_access_key)

volumes = ec2_conn.get_all_volumes()

for volume in volumes:
    nod = int(volume.tags.get(tag_id, 0))
    keep_after = datetime.datetime.now() - datetime.timedelta(nod)
    if nod:
        snaps = volume.snapshots()
        for snap in snaps:
            snap_time = datetime.datetime.strptime(snap.start_time, boto.utils.ISO8601_MS)
            if snap.description == "Auto Snapshot Backup" and snap_time < keep_after:
                logging.info("Deleting Snap: %s for Volume: %s" % (str(snap.id), str(volume.id)))
                snap.delete()
            else:
                logging.debug("Keeping Snap: %s for Volume: %s" % (str(snap.id), str(volume.id)))
