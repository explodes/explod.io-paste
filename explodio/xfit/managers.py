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
    pass

class WODExerciseManager(managers.QuerySetManager):
    pass

class UserWODManager(managers.QuerySetManager):
    pass
