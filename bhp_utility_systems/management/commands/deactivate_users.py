import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from bhp_personnel.models import Employee


class Command(BaseCommand):
    help = 'Deactivate users from a CSV file (identifier, email, and/or username).'

    def add_arguments(self, parser):
        parser.add_argument('--csv', required=True, help='Path to the CSV file.')
        parser.add_argument('--dry-run', action='store_true', help='Preview without saving.')

    def handle(self, *args, **options):
        csv_path = options['csv']
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('--- DRY RUN — no changes will be saved ---'))

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                rows = [{k.strip().lower(): v.strip() for k, v in row.items()}
                        for row in csv.DictReader(f)]
        except FileNotFoundError:
            raise CommandError(f'CSV file not found: {csv_path}')

        deactivated, not_found, already_inactive = [], [], []

        for row in rows:
            identifier = row.get('identifier', '')
            email = row.get('email', '')
            username = row.get('username', '')

            if not any([identifier, email, username]):
                continue

            user = self._resolve_user(identifier, email, username)

            if user is None:
                not_found.append(self._label(identifier, email, username))
            elif not user.is_active:
                already_inactive.append(user.username)
            else:
                if not dry_run:
                    user.is_active = False
                    user.save()
                deactivated.append(user.username)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Deactivated ({len(deactivated)}): {", ".join(deactivated) or "none"}'))
        self.stdout.write(self.style.WARNING(
            f'Already inactive ({len(already_inactive)}): {", ".join(already_inactive) or "none"}'))
        self.stdout.write(self.style.ERROR(
            f'Not found ({len(not_found)}): {", ".join(not_found) or "none"}'))

        if dry_run:
            self.stdout.write(self.style.WARNING('--- DRY RUN complete — no changes saved ---'))

    def _resolve_user(self, identifier, email, username):
        if identifier:
            emp = Employee.objects.filter(identifier=identifier).first()
            if emp:
                user = User.objects.filter(email=emp.email).first()
                if user:
                    return user
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                return user
        if username:
            return User.objects.filter(username=username).first()
        return None

    def _label(self, identifier, email, username):
        return '/'.join(filter(None, [identifier, email, username])) or 'unknown'
