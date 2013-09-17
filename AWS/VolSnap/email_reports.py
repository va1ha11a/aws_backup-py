"""Generate emails from reports to alert admins to potential issues"""

from jinja2 import Template
from reports import expires_future
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

def main():
    mailer = MailUtils()
    html = expires_tomorrow()
    return mailer.send_mail(settings.email_from, "Expiry Report", html, settings.email_to, html_body=html)

 
if __name__ == "__main__":
    print main()
    


    