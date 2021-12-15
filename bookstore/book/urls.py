from django.urls import path
from book import views

urlpatterns = [

    path('books',views.BookMixinList.as_view()),
    path('books/int:<id>', views.BookDetailMixins.as_view()),
    path('books/accounts/signup',views.UserCreationView.as_view()),
    path('books/accounts/signin',views.SignInView.as_view()),




]