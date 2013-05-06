import boto.utils, boto.ec2, time, datetime
from datetime import timedelta
from botocreds import aws_access_key_id, aws_secret_access_key

ec2_conn = boto.ec2.connect_to_region("ap-southeast-2", 
                                      aws_access_key_id=aws_access_key_id, 
                                      aws_secret_access_key=aws_secret_access_key)

volumes = ec2_conn.get_all_volumes()

tag_id = "BU"

for volume in volumes:
    butime = int(volume.tags.get(tag_id, 0))
    if butime:
        snaps = volume.snapshots()
        for snap in snaps:
            snap_time =  datetime.datetime.strptime(snap.start_time, boto.utils.ISO8601_MS)
            snap_due = snap_time + timedelta(hours=butime)
            due_now = snap_due < datetime.datetime.utcnow()
        print snaps
        if due_now:
            print "Snapping...(Disabled) " + str(volume.id)
            #volume.create_snapshot('Auto Snapshot Backup')


            
