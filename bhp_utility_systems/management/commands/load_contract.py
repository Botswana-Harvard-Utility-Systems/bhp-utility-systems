import csv
from datetime import datetime as dt
from django.core.management.base import BaseCommand
from bhp_personnel.models import Contract, Contracting, JobDescription, Employee
from bhp_personnel.models.list_models import Skills


class Command(BaseCommand):
    help = 'load employee contract'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Data fine path, csv file')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['file_path']
        self._load_data(csv_path)

    def _load_data(self, csv_path: str):
        with open(csv_path, 'r', newline='') as csv_file:
            counter = 0
            reader = csv.DictReader(csv_file)
            contracts_data = []
            for row in reader:
                try:
                    employee_instance = Employee.objects.get(employee_code=row.get('Employee_code'))
                except Employee.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'Employee with code {row.get("Employee_code")} not found. Skipping row {counter + 1}.'))
                    continue

                start_date = dt.strptime(row.get('start_date', ''), '%Y-%m-%d').date() if row.get('start_date') else None
                end_date = dt.strptime(row.get('end_date', ''), '%Y-%m-%d').date() if row.get('end_date') else None

                # Check for duplicate contract

                contract = Contract.objects.update_or_create(
                    identifier=employee_instance.identifier,
                    duration=row.get('duration'),
                    start_date=start_date,
                    end_date=end_date,
                    status=row.get('status'),
                    contract_ended=bool(row.get('contract_ended', False)),
                )

                counter += 1
                print(f"Row {counter}")

                contracts_data.append({
                    'contract': contract,
                    'job_title': row.get('job_title'),
                    'skills': row.get('skills').split(',')
                })

            for contract_data in contracts_data:
                try:
                    job_description = JobDescription.objects.get(job_title=contract_data['job_title'])
                except JobDescription.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'Job title {contract_data["job_title"]} not found.'))
                    continue

                contracting = Contracting(
                    contract=contract_data['contract'],
                    job_description=job_description,
                )
                contracting.save()

                for skill in contract_data['skills']:
                    try:
                        skill_instance = Skills.objects.get(skills=skill)
                        contracting.skills.add(skill_instance)
                    except Skills.DoesNotExist:
                        self.stderr.write(self.style.WARNING(f'Skill {skill} not found.'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
