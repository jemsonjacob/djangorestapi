from django.urls import path

from reporting import views




urlpatterns=[
      path('report/accounts/signup',views.UserCreationView.as_view()),
      path('report/accounts/signin',views.SignInView.as_view()),
]