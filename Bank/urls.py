from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('withdraw/<thro>/', views.withdrw, name='withdrw'),
    path('deposit/<thro>/', views.deps, name='deps'),
    path('history/<thro>', views.hists, name='hists'),
    path('account/', views.hume, name='hume'),
    path('logout/', views.logout, name='logout'),
]
