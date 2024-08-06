from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('user/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('user/phone/<str:phone>/', views.get_user_by_phone, name='get_user_by_phone'),
    path('user/email/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('users/', views.display_all_users, name='display_all_users'),
    path('users/address/<str:address>/', views.get_users_by_address, name='get_users_by_address'),
    path('users/role/<str:role>/', views.get_users_by_role, name='get_users_by_role'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/total/', views.get_total_users, name='get_total_users'),
    path('users/statistics/', views.user_growth_statistics, name='user_growth_statistics'),
    path('password/reset/', views.reset_password, name='reset_password'),
    path('update/<int:id>', views.update_user, name='update_user'),  # New URL for updating a user
    path('logout/', views.logout, name='logout'),  # New URL for logging out
]

