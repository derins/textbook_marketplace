from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Book
from users.models import CustomUser
from  django.core.validators import RegexValidator


class EditProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        
        fields = ['username','email','first_name','last_name', 'phone', 'password']

class CreateListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.seller = kwargs.pop('seller', None)
        super(CreateListingForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'isbn_number', 'book_type', 'subject', 'edition_number']
    
    name = forms.CharField(label='Book Name', max_length=50)
    author = forms.CharField(label='Author', max_length=50)
    isbn_number = forms.IntegerField(label = "ISBN Number")
    price = forms.DecimalField(label="Price", max_digits = 8, decimal_places = 2, initial="0.00")
#    isbn_number = forms.CharField(label="ISBN Number", max_length=20, validators=[
#      RegexValidator(
#                     regex=r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
#                     message='Please enter a valid ISBN-10 or ISBN-13',
#                     ),
#      ])
    book_type = forms.ChoiceField(choices = (('hardCover', 'Hard Cover'), ('looseLeaf', 'Loose Leaf'), ('paperBack', 'Paper Back'), ('pdf', 'PDF')))


class EditListingForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'isbn_number', 'book_type', 'subject', 'edition_number']
    
    name = forms.CharField(label='Book Name', max_length=50)
    author = forms.CharField(label='Author', max_length=50)
    price = forms.DecimalField(label = 'Price' )
    isbn_number = forms.IntegerField(label = "ISBN Number")
#    isbn_number = forms.CharField(label="ISBN Number", max_length=20, validators=[
#      RegexValidator(
#                     regex=r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
#                     message='Please enter a valid ISBN-10 or ISBN-13',
#                     ),
#      ])
    book_type = forms.ChoiceField(choices = (('hardCover', 'Hard Cover'), ('looseLeaf', 'Loose Leaf'), ('paperBack', 'Paper Back'), ('pdf', 'PDF')))
