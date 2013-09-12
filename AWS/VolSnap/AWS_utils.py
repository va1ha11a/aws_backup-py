#!/usr/bin/env python
""""Utils that connect to AWS"""

import logging
logger = logging.getLogger(__name__)

import boto.utils, boto.ec2, boto.ses
import settings, datetime
import distutils.util

class SnapUtils:
    _ec2_conn = boto.ec2.connect_to_region(settings.target_region, 
                                          aws_access_key_id=settings.aws_access_key_id, 
                                          aws_secret_access_key=settings.aws_secret_access_key)

    def _bt_to_dt(self, boto_time):
        """Convert aws/boto time into a proper python datetime object"""
        logger.debug("Convert time from boto format to python datetime: " + str(boto_time))
        dt = datetime.datetime.strptime(boto_time, boto.utils.ISO8601_MS)
        return dt

    def _get_bu_tags_from_snap(self, snapshot):
        """Get tags from snapshot to determine the backup level of that snap """
        logger.info("Getting tags from snapshot: " + str(snapshot))
        tags = {bu_tag:distutils.util.strtobool(snapshot.tags.get(val, "False")) for bu_tag, val in settings.snap_tags.iteritems()}
        return tags

    def get_vols_for_backup(self):
        """Get a list of all volumes that have the backup enabled tag set to True"""
        logger.info("Getting list of volumes with backup enabled")
        all_vols = self._ec2_conn.get_all_volumes(filters={"tag:"+settings.backup_enabled_tag:True})
        return [{"id":vol.id, "policy":vol.tags[settings.backup_policy_tag]} for vol in all_vols]
    
    def get_snaps_for_vol(self, volume_id):
        """Get a list of snapshots matching a given volume id and description 
        and status defined in settings."""
        logger.info("Getting list of existing snapshots for volume: " + str(volume_id))
        snaps = self._ec2_conn.get_all_snapshots(filters={"volume_id":volume_id, 
                                                          "description":settings.desc, 
                                                          "status":settings.complete_status})
        snaps_details = [{"bu-keys":self._get_bu_tags_from_snap(snap), "id":snap.id, "start_time":self._bt_to_dt(snap.start_time)} for snap in snaps]
        return snaps_details

    def create_snap_for_vol(self, volume_id, bu_keys):
        """Create a snapshot and tag as per due"""
        logger.info("Create a snapshot and tag as per due. Volume: " + str(volume_id))
        logger.debug("Tags: " + str(bu_keys))
        vol_obj = self._ec2_conn.get_all_volumes(volume_id)[0]
        snap = vol_obj.create_snapshot(settings.desc)
        for key, value in bu_keys.iteritems():
            if value:
                snap.add_tag(settings.snap_tags[key], value)
        return snap.id

class MailUtils:
    """Utilities for working with email via the AWS SES interface"""
    _ses_conn = boto.ses.connect_to_region(settings.ses_region, 
                                            aws_access_key_id=settings.aws_access_key_id, 
                                            aws_secret_access_key=settings.aws_secret_access_key)
    def send_mail(self, *args, **kwargs):
        """Function to send mail"""
        logger.info("Sending Email")
        result = self._ses_conn.send_email(*args, **kwargs)
        return result


if __name__ == "__main__":
    x = SnapUtils()
    vols = x.get_vols_for_backup()
    y = x.get_snaps_for_vol(vols[0]["id"])
    print vols
    print y
    

