from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--name', dest='name', default='')

    def handle(self, *args, **options):
        name = options.get('name', '')
        options['name'] = name
        return super().handle(*args, **options)
