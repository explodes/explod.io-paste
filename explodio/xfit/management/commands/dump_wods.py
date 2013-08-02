from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Dump Workout data w/o User data...'

    dump_models = (
        'xfit.Unit',
        'xfit.Gym',
        'xfit.Workout',
        'xfit.Exercise',
        'xfit.WorkoutExercise',
        'xfit.WorkoutOfTheDay',
    )

    def handle(self, *args, **options):
        from django.core.management import call_command

        if 'indent' not in options:
            options['indent'] = 2

        call_command('dumpdata', *self.dump_models, **options)