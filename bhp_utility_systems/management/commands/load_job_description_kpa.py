import json
from django.core.management.base import BaseCommand
from bhp_personnel.models import JobDescription, JobDescriptionKpa


class Command(BaseCommand):
    help = 'Load JobDescriptionKPA data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']

        with open(json_file, 'r') as file:
            job_description_kpa_data = json.load(file)

        for data in job_description_kpa_data:
            job_description_kpa_fields = data['fields']
            job_description_kpa_id = data['pk']

            try:
                job_description = JobDescription.objects.get(pk=job_description_kpa_fields['job_description'])
                job_description_kpa_fields['job_description'] = job_description
            except JobDescription.DoesNotExist:
                self.stderr.write(self.style.WARNING(f'JobDescription with id {job_description_kpa_fields["job_description"]} not found. Skipping row'))
                continue

            job_description_kpa_fields.pop('site', None)

            _, created = JobDescriptionKpa.objects.update_or_create(id=job_description_kpa_id, defaults=job_description_kpa_fields)

            if created:
                action = "created"
            else:
                action = "updated"

            self.stdout.write(self.style.SUCCESS(f'{action} JobDescriptionKPA record with id {job_description_kpa_id}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(job_description_kpa_data)} JobDescriptionKPA records'))
