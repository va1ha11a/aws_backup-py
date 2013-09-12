from botocreds import aws_access_key_id, aws_secret_access_key

#AWS Connection Settings:
target_region = "ap-southeast-2"
ses_region = 'us-east-1'

#Volume Settings:
backup_enabled_tag = "BU-E"
backup_policy_tag = "BU-P"

#Snapshot Settings:
desc = "Auto Snapshot Backup"
complete_status = "completed"
snap_tags = {"hourly":"BU-H",
             "daily":"BU-D",
             "weekly":"BU-W",
             "monthly":"BU-M",
             "yearly":"BU-Y",
             }

#Scheduling Settings:
due_resolution_mins = 15

#Logging
import logging
log_file_name = "VolSnap.log" 
log_level = logging.INFO