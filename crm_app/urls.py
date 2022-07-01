from django.urls import path
from . import views


urlpatterns = [
    path('new', views.new),
    path('new_customer', views.add),
    path('all_customers',views.all_customers),
    path('search',views.search),
    path('search/result',views.result),
    path('search_user', views.search_user),
    path("search/user_result",views.user_reuslt),
    path("edit_cust/<cust_id>",views.edit_customer),
    path('update_cust/<this_cust_id>',views.update_cust),
    path('delete/<user_id>',views.delete_customer),
    path('details/<c_id>',views.customer_details),
    path('new_service', views.new_service),
    path('add_service', views.add_service),
    path('all_services',views.all_services),
    path('edit_serv/<serv_id>', views.edit_serv),
    path('update_serv/<this_serv_id>', views.update_serv),
    path('delete_serv/<serv_id>',views.delete_serv),
    path('search_serv', views.search_serv),
    path('search/serv_result', views.serv_reuslt),
    path('offers',views.offers),
    path('cust_serv/<cust_id>',views.customer_services),
    path('add/<cust_id>/<serv_id>',views.add_service_to_cust),
    path('delete/<cust_id>/<serv_id>',views.delete_service_from_cust),

   

]