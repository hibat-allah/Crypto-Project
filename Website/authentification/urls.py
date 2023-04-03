from django.contrib import admin
from django.urls import path
from authentification import views
from django.contrib.auth.views import LoginView,LogoutView
from app.views import dashboard

#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('',views.home_view,name=''),
    path('index/', views.index_views,name='index'),

    path('adminclick', views.adminclick_view),
    path('advclick', views.advclick_view),
    path('psclick', views.psclick_view),

    path('adminsignup', views.admin_signup_view),
    path('advsignup', views.adv_signup_view),
    path('pssignup', views.ps_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='user/adminlogin.html')),
    path('advlogin', LoginView.as_view(template_name='user/advlogin.html')),
    path('pslogin', LoginView.as_view(template_name='user/pslogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='user/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-adv', views.admin_adv_view,name='admin-adv'),
    path('admin-view-adv', views.admin_view_adv_view,name='admin-view-adv'),
    path('admin-approve-adv', views.admin_approve_adv_view,name='admin-approve-adv'),
    path('approve-adv/<int:pk>', views.approve_adv_view,name='approve-adv'),
    path('reject-adv/<int:pk>', views.reject_adv_view,name='reject-adv'),


    path('admin-ps', views.admin_ps_view,name='admin-ps'),
    path('admin-view-ps', views.admin_view_ps_view,name='admin-view-ps'),
    path('admin-approve-ps', views.admin_approve_ps_view,name='admin-approve-ps'),
    path('approve-ps/<int:pk>', views.approve_ps_view,name='approve-ps'),
    path('reject-ps/<int:pk>', views.reject_ps_view,name='reject-ps'),
    path('documents/',views.documents,name='documents'),

]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('adv-dashboard', views.adv_dashboard_view,name='adv-dashboard'),

]



#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('ps-dashboard', dashboard,name='ps-dashboard'),
]


