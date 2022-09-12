from django.urls import path
from . import false_views
from .views import user

urlpatterns = [
<<<<<<< HEAD
    path('/',views.getData),
    path('/register',views.registerAccount),
    path('/account/<str:username>',views.personalAccount),
    path('login/',views.loginAccount),
=======
    path('',false_views.getData),
    path('register',user.register)
>>>>>>> 424e5ecc703442d66b04dc12982fdded1d691a44
]