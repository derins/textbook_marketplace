from django.db import models
from users.models import CustomUser
from datetime import datetime
from django.conf import settings
# Create your models here.

class Book(models.Model):
    """This class represents the event model."""
    name = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits = 8, decimal_places = 2, default=0.00)
    isbn_number = models.BigIntegerField(null = True)
#    isbn_number = models.CharField(null = True, max_length=20)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null=True, on_delete = models.PROTECT)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)
    book_type = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    is_sold = models.BooleanField(null=True)
    edition_number = models.PositiveIntegerField(null=True)
    starred_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name='starred_by')
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

    def get_absolute_url(self):
        return "/textbook"
