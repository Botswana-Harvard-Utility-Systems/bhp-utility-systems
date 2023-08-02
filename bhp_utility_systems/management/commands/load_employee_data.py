from bhp_personnel.models import Employee, Supervisor, Department, Pi
import datetime

from dateutil import parser
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from edc_constants.constants import HIDE_FORM
import openpyxl


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Data fine path, csv file')

    def handle(self, *args, **kwargs):
        excel_path = kwargs['file_path']
        self._load_data(excel_path)

    def _load_data(self, excel_path: str):
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active

        employee_objects = dict()

        for row in sheet.iter_rows(values_only=True):

            if not row[0]:
                break
            if row[0] == 'employee_code':
                continue

            employee_code = row[0]
            last_name = row[1]
            first_name = row[2]
            department = row[3].split('|')[0]
            hod = row[3].split('|')[1]
            job_title = row[4]
            hired_date = datetime.datetime.strptime(row[5], '%d/%m/%Y')
            status = row[6]
            gender = row[7]
            cell = row[8].strip() if row[8] else None
            email = row[9]
            supervisor_first_name = row[10].split('|')[0]
            supervisor_last_name = row[10].split('|')[1]
            supervisor_email = row[10].split('|')[2]
            supervisor_cell = row[10].split('|')[3]

            if not cell:
                message = f'''\
                ------------------------------------------
                Message  : Missing contact info
                Firstname : {first_name}
                Lastname  : {last_name}
                E-Mail    : {email}'''

                self.stdout.write(
                    self.style.WARNING(message))

            else:
                try:
                    supervisor = Supervisor.objects.get(
                        first_name=supervisor_first_name,
                        last_name=supervisor_last_name,)
                except Supervisor.DoesNotExist:
                    supervisor = Supervisor.objects.create(
                        first_name=supervisor_first_name,
                        last_name=supervisor_last_name,
                        cell=supervisor_cell,
                        email=supervisor_email)

                dept, _ = Department.objects.get_or_create(
                    hod=hod,
                    dept_name=department)

                if job_title.lower() == 'principal investigator':

                    principal_investigator_exists = Pi.objects.filter(email=email,
                                                                      first_name=first_name,
                                                                      last_name=last_name,).exists()

                    if not principal_investigator_exists:
                        Pi.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            gender=gender,
                            hired_date=hired_date,
                            cell=cell

                        )

                        message = f'''\
                        ------------------------------------------
                        Message   : Principal investigator created 
                        Firstname : {first_name}
                        Lastname  : {last_name}
                        E-Mail    : {email} '''

                        self.stdout.write(
                            self.style.SUCCESS(message))

                else:

                    try:
                        Employee.objects.get(email=email,
                                             first_name=first_name,
                                             last_name=last_name)
                    except Employee.DoesNotExist:

                        Employee.objects.create(
                            employee_code=employee_code,
                            email=email,
                            job_title=job_title,
                            supervisor=supervisor,
                            hired_date=hired_date,
                            gender=gender,
                            department=dept,
                            first_name=first_name,
                            last_name=last_name,
                            cell=cell

                        )
                        message = f'''\
                        ------------------------------------------
                        Message   : Employee created 
                        Firstname : {first_name}
                        Lastname  : {last_name}
                        E-Mail    : {email} '''

                        self.stdout.write(
                            self.style.SUCCESS(message))

                    else:

                        message = f'''\
                        ------------------------------------------
                        Message   : Employee already exist
                        Firstname : {first_name}
                        Lastname  : {last_name}
                        E-Mail    : {email}'''

                        self.stdout.write(
                            self.style.WARNING(message))
