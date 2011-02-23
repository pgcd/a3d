from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Macro(models.Model):
    name=models.CharField(max_length=50, unique=True)
    regex_match=models.TextField(verbose_name=_('regular expression'), blank=True)
    regex_replace=models.TextField(verbose_name=_('replacement expression'), blank=True)
    description=models.TextField(verbose_name=_('extended description'), blank=True)

    def __unicode__(self):
        return self.name
#Further improvements might include _automagic_ macros (and profanity filters)
