from django.db import models
from django.utils.translation import gettext_lazy as _

class CourseTypeChoice(models.TextChoices):
        NONE = 'NONE',_('NONE')
        MATH = 'MTH',_('MATH')