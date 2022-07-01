from django.urls import path
from . import views
urlpatterns = [
    path('', views.form),
    path('register',views.register),
    path('all_employee',views.all_users),
    path('login', views.login),
    path('edit/<user_id>', views.edit_user),
    path('update/<user_id>', views.update_user),
    path('delete/<user_id>', views.delete_user),
    path('logout', views.logout),
]