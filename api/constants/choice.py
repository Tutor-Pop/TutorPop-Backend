from django.db import models
from django.utils.translation import gettext_lazy as _

class CourseTypeChoice(models.TextChoices):
        NONE = 'NONE',_('NONE')
        MATH = 'MATH',_('MATH')
        GENERAL = 'GENERAL',_('GENERAL')
        SCIENCE = 'SCIENCE',_('SCIENCE')
        LANGUAGE = 'LANGUAGE',_('LANGUAGE')
        MUSIC = 'MUSIC',_('MUSIC')
        COOK = 'COOK',_('COOK')
        FINANCE = 'FINANCE',_('FINANCE')