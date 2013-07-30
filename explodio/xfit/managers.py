from explodio.common import managers


class GymManager(managers.ActiveQuerySetManager):
    """
    Custom manger for Gyms
    """

    class QuerySet(managers.ActiveQuerySet):

        def for_user(self, user):
            """
            Filter for a specific user
            :param user: User who may have subscribed to Gyms
            :return: QuerySet of Gym
            """
            return self

class WorkoutManager(managers.QuerySetManager):
    """
    Custom manger for Workouts
    """
    pass

class ExerciseManager(managers.QuerySetManager):
    """
    Custom manger for Exercises
    """
    pass

class WorkoutExerciseManager(managers.QuerySetManager):
    """
    Custom manger for WorkoutExercises
    """
    pass

class WorkoutOfTheDayManager(managers.QuerySetManager):
    """
    Custom manger for WorkoutOfTheDays
    """

    class QuerySet(managers.QuerySet):

        def for_day(self, day):
            """
            Filter for a specific day
            :param day: Day to filter for
            :return: QuerySet of WorkoutOfTheDay
            """
            return self.filter(day=day)

class WODExerciseManager(managers.QuerySetManager):
    """
    Custom manger for WODExercises
    """
    pass

class UserWODManager(managers.QuerySetManager):
    """
    Custom manger for UserWODs
    """

    class QuerySet(managers.QuerySet):

        def for_day(self, day):
            """
            Filter for a specific day
            :param day: Day to filter for
            :return: QuerySet of UserWOD
            """
            return self.filter(wod__day=day)

        def for_user(self, user):
            """
            Filter for a specific user
            :param user: User who has accomplished WODs
            :return: QuerySet of UserWOD
            """
            return self.filter(user=user)
