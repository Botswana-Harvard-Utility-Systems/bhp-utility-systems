import json
from django.core.management.base import BaseCommand
from bhp_personnel.models import JobDescription
from bhp_personnel.models import Department


class Command(BaseCommand):
    help = 'Load JobDescription data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r') as file:
            job_descriptions_data = json.load(file)

        for data in job_descriptions_data:
            job_description_fields = data['fields']
            job_description_fields['id'] = data['pk']
            job_description_fields.pop('site', None)

            try:
                department = Department.objects.get(pk=job_description_fields['department'])
                job_description_fields['department'] = department
            except Department.DoesNotExist:
                self.stderr.write(self.style.WARNING(f'Department with id {job_description_fields["department"]} not found. Skipping row {job_description_fields["id"]}.'))
                continue

            job_description = JobDescription(**job_description_fields)
            job_description.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(job_descriptions_data)} JobDescription records'))
