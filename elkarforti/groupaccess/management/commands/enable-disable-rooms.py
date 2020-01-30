from django.core.management.base import BaseCommand, CommandError
from groupaccess.models import FortiGroup


class Command(BaseCommand):
    help = 'Enable or disable all FortiGroups'

    def add_arguments(self, parser):
        parser.add_argument('action', type=int, help='1 indicates enable, and 0 indicates disable')

    def handle(self, *args, **options):
        action = options['action']
        if action == 1:
            FortiGroup.objects.all().update(enabled=True)
        else:
            FortiGroup.objects.all().update(enabled=False)

        # We only need to save one of them using the Models save methond because the save method will check all groups state and it will create a payload to save in Forti all objets state

        group = FortiGroup.objects.order_by('name').first()
        if action==1:
            group.enabled = True
        else:
            group.enabled = False

        group.save()
