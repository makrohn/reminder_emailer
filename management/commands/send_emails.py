"""
Script to send emails to manager of employees who have separated,
warning them that the employee's Google account is pending deletion
"""

from django.core.management.base import BaseCommand, CommandError
import smtplib
from email.mime.text import MIMEText
from emailer import settings
import datetime
from emailer.models import separatedEmployee


def send_email(name, email, time):
    """Send an email to a manager regarding their employee"""
    days_remaining = settings.deletion_day - time
    if days_remaining == 1:
        time_string = "tomorrow"
    else:
        time_string = "in %s days" % days_remaining
    msg = MIMEText(
        "TEST MESSAGE Hi! The Google account for " +
        name +
        " is due to be deleted " +
        time_string
        )
    msg['Subject'] = "Pending Google account deletion for " + name
    msg['From'] = settings.from_address
    msg['To'] = email
    s = smtplib.SMTP(settings.smtp_server)
    s.sendmail(
        settings.from_address,
        [email],
        msg.as_string(),
        )


def process_matching_employees(days):
    """Find employees who left a certain number of days ago"""
    today = datetime.date.today()
    warning_date = today - datetime.timedelta(days)
    alerts = separatedEmployee.objects.filter(set_date=warning_date)
    return alerts


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key in settings.reminder_dates:
            if settings.reminder_dates[key] < settings.deletion_day:
                alerts = process_matching_employees(settings.reminder_dates[key])
                for employee in alerts:
                    send_email(
                        employee.name,
                        employee.manager_email,
                        settings.reminder_dates[key],
                        )
