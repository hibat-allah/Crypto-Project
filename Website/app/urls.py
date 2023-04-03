# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    re_path(r'^formateurs/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.FormateurView.as_view(),
            name='formateurs'),
    re_path(r'^files/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.FileView.as_view(),
            name='files'),       
    re_path(r'^formations/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.FormationView.as_view(),
            name='formations'),
    re_path(r'^beneficiaires/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.BeneficiaireView.as_view(),
            name='beneficiaires'),
    re_path(r'^clients/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.ClientView.as_view(),
            name='clients'),
    re_path(r'^themes/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.ThemeView.as_view(),
            name='themes'),
    re_path(r'^domaines/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.DomaineView.as_view(),
            name='domaines'), 
    path('create_domaine/', views.create_domaine, name="create_domaine"),
    path('create_theme/', views.create_theme, name="create_theme"),
    path('create_formateur/', views.create_formateur, name="create_formateur"),
    path('create_file/', views.create_file, name="create_file"),
    path('create_formation/', views.create_formation, name="create_formation"),
    path('create_client/', views.create_client, name="create_client"),
    path('create_beneficiaire/', views.create_beneficiaire, name="create_beneficiaire"),   
    path('exportcsv_domaines/', views.exportcsv_domaines, name="exportcsv_domaines"),
    path('exportcsv_themes/', views.exportcsv_themes, name="exportcsv_themes"),
    path('exportcsv_formateurs/', views.exportcsv_formateurs, name="exportcsv_formateurs"),
    path('exportcsv_files/', views.exportcsv_files, name="exportcsv_files"),
    path('exportcsv_formations/', views.exportcsv_formations, name="exportcsv_formations"),
    path('exportcsv_clients/', views.exportcsv_clients, name="exportcsv_clients"),
    path('exportcsv_beneficiaires/', views.exportcsv_beneficiaires, name="exportcsv_beneficiaires"),
    path('ajax/load-formateurs/', views.load_formateurs, name='ajax_load_formateurs'),
    path('ajax/load-theme/', views.load_theme, name='ajax_load_theme'),
    path('ajax/load-formateurs_bis/', views.load_formateurs_bis, name='ajax_load_formateurs_bis'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

] 
