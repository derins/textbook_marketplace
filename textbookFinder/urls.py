from django.urls import path
from django.urls import include, path

from . import views

app_name = 'textbookFinder'
urlpatterns = [
    path('', views.BookListView.as_view(template_name="index.html"),name = 'index'),
    path('create', views.BookCreateView.as_view(template_name="create.html"), name = 'create'),
    path('listing/<int:pk>', views.ListingsView.as_view(template_name="listing.html"), name="listing"),
    path('account/<int:pk>', views.AccountView.as_view(template_name="account.html"), name="account"),
    path('cart', views.ListCartView.as_view(template_name="cart.html"), name="cart"),
    path('cart/add/<int:pk>', views.add_to_cart, name="cart_add"),
    path('cart/remove/<int:pk>', views.remove_from_cart, name="cart_remove"),
    path('account/<int:pk>/edit', views.EditView, name="edit"),
    path('account/<int:pk>/edit/password', views.ChangePassword, name="password"),
    path('remove_listing/<int:pk>', views.remove_listing, name = "remove_listing"),
    path('mark_sold/<int:pk>',views.mark_sold, name = "mark_sold"),
    path('edit_listing/<int:pk>',views.edit_listing, name = "edit_listing"),
    path('my_listing',views.MyListingView.as_view(template_name="mylisting.html"), name = "my_listings"),
    path('email/<int:pk>', views.send_email, name="send_email")
]
