from django.urls import path

from reporting import views




urlpatterns=[
      path('reporting/accounts/signup',views.UserCreateMixin.as_view()),
      path('reporting/accounts/signin',views.SigninView.as_view()),
]