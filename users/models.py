from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import * 


telephone = RegexValidator(r'^[0-9]\d{2}-\d{3}-\d{4}$', 'Only numeric characters are allowed.')
mail = RegexValidator(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', 'Needs @.')


class CustomUser(AbstractUser):
    """This class represents the user model."""
    
    email = models.CharField(max_length=254, validators=[mail, MaxLengthValidator], blank=False)
    """purchased_books = models.ForeignKey("textbookFinder.Book", on_delete = models.PROTECT, related_name = 'purchased_books', null=True)"""
    
    phone = models.CharField(max_length=18, validators=[telephone, MaxLengthValidator], blank = True)
    
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return self.email

