"""Generate emails from reports to alert admins to potential issues"""

from jinja2 import Template
from reports import expires_future, latest_snap_all_vols
import settings
import datetime
from dateutil.relativedelta import relativedelta
from AWS_utils import MailUtils


generic_template = Template("""
<html>
<body>
<h2>{{ doc_heading }}</h2>
<table border='1' cellpadding="4">
    <tr>
        {% for header in headers %}<th>{{header}}</th>{% endfor %}
    </tr>
    {% for item in details %}
        <tr>
        {% for col in cols %}<td>{{item[col]}}</td>{% endfor %}
        </tr>
    {% endfor %}
</table>
</body>
</html>
""")

def expires_tomorrow():
    """Create HTML table of backup images due to expire in the next day."""
    now_utc = datetime.datetime.utcnow()
    tomorrow_utc = now_utc + relativedelta(days=1)
    details = expires_future(tomorrow_utc)
    cols = ['id', 'start_time', 'expiry', 'bu_keys']
    headers = ['ID', 'Start Time', 'Image Expiry', 'Backup Type']
    doc_heading = "AWS Backups due to expire between: %s - %s (UTC)" % (str(now_utc), str(tomorrow_utc))
    result = generic_template.render(details=details, 
                                     cols=cols, 
                                     headers=headers, 
                                     doc_heading=doc_heading)
    return result

def vols_not_snapped_today():
    """Create a HTML list of vols that have not had snapshots in the last day."""
    latest = latest_snap_all_vols()
    now_utc = datetime.datetime.utcnow()
    yesterday_utc = now_utc - relativedelta(days=1)
    details = [{'vol_id':vol, 'last':date} for vol, date in latest.iteritems() if date == None or date < yesterday_utc]
    cols = ['vol_id', 'last']
    headers = ['Volume ID', 'Last Snapshot Time']
    doc_heading = "AWS Volumes with no successfull snapshots since: %s (UTC)" % (str(yesterday_utc)) 
    result = generic_template.render(details=details, 
                                     cols=cols, 
                                     headers=headers, 
                                     doc_heading=doc_heading)
    return result

def mail_report(title, func, mailer):
    """Mail a report given its HTML generation function and title."""
    html = func()
    results = mailer.send_mail(settings.email_from, title, html, settings.email_to, html_body=html)
    return results

report_map = {"Expiry Report":expires_tomorrow,
              "Missing Snapshots Report":vols_not_snapped_today}

def main():
    results = []
    mailer = MailUtils()
    
    for title in settings.enabled_reports:
        func = report_map[title]
        results.append(mail_report(title, func, mailer))
    
    return results 

 
if __name__ == "__main__":
    print main()
    


    