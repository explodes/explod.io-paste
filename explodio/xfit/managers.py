from explodio.common import managers


class GymManager(managers.ActiveQuerySetManager):
    """
    Custom manger for Gyms
    """

    class QuerySet(managers.ActiveQuerySet):

        def subscribed_by(self, user):
            """
            Filter for a specific user
            :param user: User who may have subscribed to Gyms
            :return: QuerySet of Gym
            """
            return self

class GymLocationManager(managers.ActiveQuerySetManager):
    """
    Custom manger for Gym Locations
    """

    class QuerySet(managers.ActiveQuerySet):

        def subscribed_by(self, user):
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

        def active(self):
            """
            Filter by WorkoutOfTheDays with active Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(gym__active=True)

        def inactive(self):
            """
            Filter by WorkoutOfTheDays with inactive Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(gym__active=False)

        def for_day(self, day):
            """
            Filter for a specific day
            :param day: Day to filter for
            :return: QuerySet of WorkoutOfTheDay
            """
            return self.filter(day=day)

class UserWODManager(managers.QuerySetManager):
    """
    Custom manger for UserWODs
    """

    class QuerySet(managers.QuerySet):

        def active(self):
            """
            Filter by UserWODs with WODs with active Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(wod__gym__active=True)

        def inactive(self):
            """
            Filter by UserWODs with WODs with inactive Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(wod__gym__active=False)

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

class WODExerciseManager(managers.QuerySetManager):
    """
    Custom manger for WODExercises
    """

    class QuerySet(managers.QuerySet):

        def active(self):
            """
            Filter by WODExercises with WODs with active Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(user_wod__wod__gym__active=True)

        def inactive(self):
            """
            Filter by WODExercises with WODs with inactive Gyms
            :return: QuerySet of UserWOD
            """
            return self.filter(user_wod__wod__gym__active=False)
