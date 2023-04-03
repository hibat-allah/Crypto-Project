# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.fields.related import ForeignKey
from django.forms import CharField,IntegerField
from app.choices import *

class Domaine(models.Model):
    code = models.CharField(max_length=15)
    nom = models.CharField(max_length=40, unique=True) 
    def set_code(self, val):
        self.code = val
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = 'domaine'
        verbose_name_plural = 'domaines'    
class Theme(models.Model):
    code = models.CharField(max_length=15)
    nom = models.CharField(max_length=50, unique=True)
    domaine = models.ForeignKey('Domaine',on_delete=models.CASCADE)
    def set_code(self, val):
        self.code = val
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = 'theme'
        verbose_name_plural = 'themes'
class Client(models.Model):
    code = models.CharField(max_length=15)
    nom=models.CharField(max_length=50, unique=True)
    email= models.EmailField(max_length=254)
    phone= models.CharField( max_length=10)
    def set_code(self, val):
        self.code = val
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'    
class Beneficiaire(models.Model):
    CN = models.IntegerField(unique=True)
    nom = models.CharField( max_length=50)
    prenom = models.CharField(max_length=40)
    adresse = models.CharField(max_length=50)
    email= models.EmailField(max_length=254)
    phone= models.CharField( max_length=10)
    datenaissance= models.DateField()
    genre = models.CharField(max_length = 8, choices = GENRE_CHOICES, default=1)
    client= models.ForeignKey("Client", on_delete=models.CASCADE)
    def __str__(self):
        return self.nom+' '+self.prenom
    class Meta:
        verbose_name = 'beneficiaire'
        verbose_name_plural = 'beneficiaires'
class Formation(models.Model):
    code = models.CharField(max_length=15)
    nom = models.CharField(max_length=50, unique=True)
    formateur=models.ForeignKey("Formateur",on_delete=models.CASCADE)
    theme=models.ForeignKey("Theme",on_delete=models.CASCADE)
    client=models.ForeignKey("Client",on_delete=models.CASCADE)
    statut = models.CharField(max_length = 20, default="non commencé")
    active = models.BooleanField(default = False)
    def set_code(self, val):
        self.code = val
    def __str__(self):
        return self.nom
    def set_statut(self, val):
        self.statut = val
    def set_active(self, val):
        self.active = val
    class Meta:
        verbose_name = 'formation'
        verbose_name_plural = 'formations'
        unique_together = ('formateur', 'theme','client')

class Formateur(models.Model):
    CN = models.IntegerField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=50)
    adresse= models.CharField(max_length=50)
    email= models.EmailField(max_length=254)
    phone= models.CharField( max_length=10)
    datenaissance= models.DateField()
    genre = models.CharField(max_length = 8, choices = GENRE_CHOICES, default=1)
    theme=models.ManyToManyField(Theme, related_name = 'formateur_theme_set')
    CV = models.FileField(upload_to='')
    def __str__(self):
        return self.nom+' '+self.prenom 

    class Meta:
        verbose_name = 'formateur'
        verbose_name_plural = 'formateurs'
        
class File(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='')
    def __str__(self):
        return self.file_name
        
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs) 
        
    class Meta:
        verbose_name = 'file'
        verbose_name_plural = 'files'    
    
class Salle(models.Model):
    active = models.BooleanField(default = True)
    def __str__(self):
        return 'Salle'+' '+str(self.id)
    def set_active(self, a):   
        self.statut = a
    class Meta:
        verbose_name = 'salle'
        verbose_name_plural = 'salles'   