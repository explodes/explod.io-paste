from explodio.xfit import models


class WODExerciseStatistics(object):

    def __init__(self, user, exercise):
        self.user = user
        self.exercise = exercise
        self.wod_exercises = models.WorkoutExercise.objects \
            .for_user(user) \
            .for_exercise(exercise)
