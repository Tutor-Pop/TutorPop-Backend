from django.urls import path
from . import views

urlpatterns = [
    path('/',views.getData),
    path('/register',views.registerAccount),
    path('/account/<str:username>',views.personalAccount),
    path('login/',views.loginAccount),
]