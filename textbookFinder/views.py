from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Book
from users.models import CustomUser
import sys, functools, operator
from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from textbookFinder.forms import EditProfileForm, EditListingForm
from django.contrib.auth import update_session_auth_hash
from .forms import CreateListingForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import BadHeaderError, send_mail


class BookListView(generic.ListView):
    model = Book
    template_name = 'index.html'

    def get_queryset(self):

    	if self.request.GET:
            searchBy = self.request.GET.get("searchBy")
            searchWord = self.request.GET.get("searchValue")
            lowerPrice = self.request.GET.get("lowerPrice")
            upperPrice = self.request.GET.get("upperPrice")
            editionNumber = self.request.GET.get("editionNum")

            filterArgs = []

            if searchBy == "title" and searchWord != "":
                print("add")
                filterArgs.append( Q(name__icontains=searchWord))
                print(filterArgs)
            elif searchBy == "author" and searchWord != "":
                filterArgs.append( Q(author__icontains=searchWord))
            elif searchBy == "class" and searchWord != "":
                filterArgs.append( Q(subject__icontains=searchWord))
            elif searchBy == "isbn" and searchWord != "":
                filterArgs.append( Q(isbn_number=searchWord))

            if upperPrice != "" and lowerPrice != "":
                filterArgs.append( Q(price__range=(lowerPrice, upperPrice)))
            elif lowerPrice != "":
                filterArgs.append( Q(price__range=(lowerPrice, sys.maxsize)))
            elif upperPrice != "":
                filterArgs.append( Q(price__range=(0, upperPrice)))

            bookTypes = []
            if self.request.GET.get("hardCover"):
                bookTypes.append("hardCover")
            if self.request.GET.get("paperBack"):
                bookTypes.append("paperBack")
            if self.request.GET.get("looseLeaf"):
                bookTypes.append("looseLeaf")
            if self.request.GET.get("pdf"):
                bookTypes.append("pdf")

            if len(bookTypes) > 0:
                filterArgs.append( Q(book_type__in=bookTypes))

            if editionNumber and searchWord != "":
                filterArgs.append( Q(edition_number=editionNumber))

            if len(filterArgs) != 0:
                if(self.request.GET.get("sort") == "LoHiPrice"):
                    return Book.objects.filter(functools.reduce(operator.and_, filterArgs)).order_by('price')
                return Book.objects.filter(functools.reduce(operator.and_, filterArgs)).order_by('-date_posted')
            else:
                if(self.request.GET.get("sort") == "LoHiPrice"):
                    return Book.objects.all().order_by('price')
                return Book.objects.all().order_by('-date_posted')
    	else:
            return Book.objects.all().order_by('-date_posted')

class BookCreateView(CreateView):
    model = Book
    template_name = 'create.html'
    form_class = CreateListingForm

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(BookCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        # pass "user" keyword argument with the current user to your form
        kwargs = super(BookCreateView, self).get_form_kwargs()
        kwargs['seller'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = self.request.user
        return super(BookCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please enter a valid ISBN-10')
        return self.render_to_response(self.get_context_data(form=form))

class AccountView(generic.DetailView):
    model = CustomUser
    template_name = "account.html"


def EditView(request, pk):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/textbook/account/'+str(pk))
        else:
            messages.info(request, 'Phone number format: xxx-xxx-xxxx')
            return redirect('/textbook/account/'+str(pk)+'/edit')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form' : form}
        return render(request, 'edit.html', args)

def ChangePassword(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/textbook/account/'+str(pk)+'/edit')
        else:
            return redirect('/textbook/account/'+str(pk)+'/password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form' : form}
        return render(request, 'password.html', args)



class ListingsView(generic.DetailView):
	model = Book
	template_name = "listing.html"

class ListCartView(generic.ListView):
    model = Book
    template_name = "cart.html"
    def get_queryset(self):
        username = None
        if self.request.user.is_authenticated:
            username = self.request.user.username
            return Book.objects.filter(starred_by__username__exact=username)
        else:
            return {}
def add_to_cart(request, pk):
    if request.user.is_authenticated:
        book = Book.objects.get(pk=pk)
        if request.user in book.starred_by.all():
            return redirect('/textbook/listing/'+str(pk)+'?saved=false')
        else:
            book.starred_by.add(request.user)
            book.save()
            return redirect('/textbook/listing/'+str(pk)+'?saved=true')
    else:
        return redirect('/users/login')
def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        book = Book.objects.get(pk=pk)
        book.starred_by.remove(request.user)
        book.save()
        return redirect('/textbook/listing/'+str(pk))
    else:
        return redirect('/users/login')
def remove_listing(request, pk):
    if request.user.is_authenticated and Book.objects.get(pk=pk).seller == request.user:
        book = Book.objects.get(pk=pk)
        book.delete()
        return redirect('/textbook/')
    else:
        return redirect('/users/login')
def mark_sold(request, pk):
    if request.user.is_authenticated and Book.objects.get(pk=pk).seller == request.user:
        book = Book.objects.get(pk=pk)
        if book.is_sold != True:
            book.is_sold = True
            book.save()
            return redirect('/textbook/')
        else:
            book.is_sold = False;
            book.save()
            return redirect('/textbook/')
    else:
        return redirect('/users/login')

def edit_listing(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        form = EditListingForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('/textbook/listing/'+str(pk))
        else:
            return redirect('/textbook/listing/'+str(pk)+'/edit')

    else:
        book = Book.objects.get(pk=pk)
        form = EditListingForm(instance=book)
        args = {'form' : form}
        return render(request, 'book_edit.html', args)

def send_email(request, pk):
    if request.method == 'POST':
        from_email = request.POST.get('fromEmail')
        buyer_name = request.POST.get('buyerName')

        book = Book.objects.get(pk=pk)
        book_name = book.name
        book_author = book.author
        book_price = book.price
        seller = book.seller.first_name + " " + book.seller.last_name


        subject = "Interest in Buying Copy of " + book.name
        to_email = book.seller.email
        message = "Hi " + book.seller.first_name + ",\nI am interested in your copy of " + book_name + " by " + book_author + " for $" + str(book_price) + ". Please let me know at " + from_email + " if the book is still available. I look forward to hearing back from you! \n-" + buyer_name

        try:
            send_mail(subject, message, from_email, [to_email])
            return redirect('/textbook/listing/'+str(pk) + '?sent=true')
        except BadHeaderError:
            return redirect('/textbook/listing/'+str(pk) + '?sent=false')
    else:
        return redirect('/textbook/listing/'+str(pk) + '?sent=false')
    

class MyListingView(generic.ListView):
    model = Book
    template_name = "mylisting.html"
    def get_queryset(self):
        username = None
        if self.request.user.is_authenticated:
            user = self.request.user
            return Book.objects.filter(seller=user)
        else:
            return {}
