from django.core.management.base import BaseCommand, CommandError

import smtplib
from email.mime.text import MIMEText
from emailer import settings
import datetime
from emailer.models import separatedEmployee


def send_email(name, email, time):
    days_remaining = settings.deletion_day - time
    if days_remaining == 1:
        time_string = "tomorrow"
    else:
        time_string = "in %s days" % days_remaining
#    print time_string
    msg = MIMEText(
        "TEST MESSAGE Hi! The Google account for " +
        name +
        " is due to be deleted " +
        time_string
        )
    msg['Subject'] = "Pending Google account deletion for " + name
    msg['From'] = settings.from_address
    msg['To'] = email
    print msg
    s = smtplib.SMTP(settings.smtp_server)
    s.sendmail(
        settings.from_address,
        [email],
        msg.as_string(),
        )


def process_matching_employees(days):
    today = datetime.date.today()
    warning_date = today - datetime.timedelta(days)
    alerts = separatedEmployee.objects.filter(set_date=warning_date)
    for employee in alerts:
        send_email(
            employee.name,
            employee.manager_email,
            days,
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key in settings.reminder_dates:
            if settings.reminder_dates[key] < settings.deletion_day:
                print key, settings.reminder_dates[key]
                process_matching_employees(settings.reminder_dates[key])
