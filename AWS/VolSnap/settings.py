from VolSnap.botocreds import aws_access_key_id, aws_secret_access_key

#AWS Connection Settings:
target_region = "ap-southeast-2"

#Volume Settings:
backup_enabled_tag = "BU-E"
backup_policy_tag = "BU-P"

#Snapshot Settings:
desc = "Auto Snapshot Backup"
complete_status = "completed"
hourly_tag = "BU-H"
daily_tag = "BU-D"
weekly_tag = "BU-W"
monthly_tag = "BU-M"
yearly_tag = "BU-Y"