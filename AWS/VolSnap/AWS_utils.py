#!/usr/bin/env python
""""Utils that connect to AWS"""

import boto.utils, boto.ec2
import settings, datetime


class AWSUtils:
    _ec2_conn = boto.ec2.connect_to_region(settings.target_region, 
                                          aws_access_key_id=settings.aws_access_key_id, 
                                          aws_secret_access_key=settings.aws_secret_access_key)

    def _bt_to_dt(self, boto_time):
        """Convert aws/boto time into a proper python datetime object"""
        dt = datetime.datetime.strptime(boto_time, boto.utils.ISO8601_MS)
        return dt

    def get_vols_for_backup(self):
        """Get a list of all volumes that have the backup enabled tag set to True"""
        all_vols = self._ec2_conn.get_all_volumes(filters={"tag:"+settings.backup_enabled_tag:True})
        return [{"id":vol.id, "policy":vol.tags[settings.backup_policy_tag]} for vol in all_vols]
    
    def get_snaps_for_vol(self, volume_id):
        """Get a list of snapshots matching a given volume id and description 
        and status defined in settings."""
        snaps = self._ec2_conn.get_all_snapshots(filters={"volume_id":volume_id, 
                                                          "description":settings.desc, 
                                                          "status":settings.complete_status})
        snaps_details = [{"id":snap.id, "start_time":self._bt_to_dt(snap.start_time)} for snap in snaps]
        return snaps_details

if __name__ == "__main__":
    x = AWSUtils()
    vols = x.get_vols_for_backup()
    y = x.get_snaps_for_vol(vols[0]["id"])
    print vols
    print y
    

