from explodio.common import managers


class GymManager(managers.ActiveQuerySetManager):
    pass

class WorkoutManager(managers.QuerySetManager):
    pass

class ExerciseManager(managers.QuerySetManager):
    pass

class WorkoutExerciseManager(managers.QuerySetManager):
    pass

class WorkoutOfTheDayManager(managers.QuerySetManager):

    class QuerySet(managers.QuerySet):

        def by_day(self, day):
            return self.filter(day=day)

class WODExerciseManager(managers.QuerySetManager):
    pass

class UserWODManager(managers.QuerySetManager):

    class QuerySet(managers.QuerySet):

        def by_day(self, day):
            return self.filter(day=day)

        def by_user(self, user):
            return self.filter(user=user)
