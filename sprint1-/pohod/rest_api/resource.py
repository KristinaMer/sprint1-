from django.db.models import IntegerChoices


class ModeratorStatus(IntegerChoices):
    new = 1,
    pending = 2,
    accepted = 3,
    rejected = 4,











