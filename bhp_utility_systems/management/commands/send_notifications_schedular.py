
from datetime import datetime
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django_q.tasks import schedule, Schedule
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Send employees notficiation emails'

    def handle(self, *args, **kwargs):
        emails = User.objects.values_list('email', flat=True)

        today = datetime(2022, 4, 28)

        subject = "Time Sheet Notifications"
        message = f"""\
            Good day

            Please be reminded to fill in your time sheet before monthend. 
            
            Best regards

            Utility System Bot
            """

        for _ in range(8):
            self._schedule_emails(
                subject=subject, 
                message=message,
                emails=emails, 
                next_run=today)

            today = today + relativedelta(months=+1)


    def _schedule_emails(self, subject, message, emails, next_run):

        schedule(
            'django.core.mail.send_mail',
            subject,
            message,
            settings.EMAIL_HOST,
            [*emails],
            schedule_type = Schedule.ONCE,
            name=f"Send Notifications : {next_run}",
            next_run=next_run,
            
        )
