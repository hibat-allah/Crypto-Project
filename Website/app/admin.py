# -*- encoding: utf-8 -*-

from django.contrib import admin
from app.models import Theme, Domaine, Formateur, Formation, Client, Beneficiaire, Salle, File
# register your models here.
admin.site.register(Theme)
admin.site.register(Domaine)
admin.site.register(Formateur)
admin.site.register(Formation)
admin.site.register(Client)
admin.site.register(Beneficiaire)
admin.site.register(Salle)
admin.site.register(File)
