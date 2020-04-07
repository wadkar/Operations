from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, Model
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_pandas.managers import DataFrameManager

# Create your models here.
#"UUID","Status","Lat","Lng"

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

class CoronaApp(Model):

    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100, blank=True, default='a')
    status = models.IntegerField(default=0)

    latitude= models.FloatField(default=0)
    longitude= models.FloatField(default=0)

    objects = DataFrameManager()

    class Meta:
        ordering = ['created']


