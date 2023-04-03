from django import forms
from app.models import Theme, Domaine, Formateur, Formation, Client, Beneficiaire, File
from app.choices import *

class DomaineForm(forms.ModelForm):
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control domaine'}))
    class Meta:
        model = Domaine
        fields = ['nom']
class ThemeForm(forms.ModelForm):
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control theme'}))
    domaine = forms.ModelChoiceField(queryset=Domaine.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select theme' 'input', 'id': 'selection'}))
    class Meta:
        model = Theme
        fields = ['nom','domaine']
        
class FormateurForm(forms.ModelForm):
    CN = forms.IntegerField(label="CN", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    prenom = forms.CharField(label="Prenom", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    phone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    adresse = forms.CharField(label="Adresse", widget=forms.TextInput(attrs={'class': 'form-control formateur'}))
    datenaissance = forms.DateField(label="DateNaissance", widget=forms.DateInput(attrs={'class': 'form-control datepicker_input formateur'}))
    genre = forms.ChoiceField(choices = GENRE_CHOICES, label="Genre", initial='', widget=forms.Select(attrs={'class': 'form-select formateur' 'input', 'id': 'selection'}), required=True)
    theme = forms.ModelMultipleChoiceField(queryset=Theme.objects.all(), widget=forms.CheckboxSelectMultiple)
    CV = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control formateur'}))
    class Meta:
        model = Formateur
        fields = ['CN','nom','prenom','email','phone','adresse','datenaissance','genre','theme','CV']
        
class FileForm(forms.ModelForm):
    file_name = forms.CharField(label="Nom Fichier", widget=forms.TextInput(attrs={'class': 'form-control file'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control file'}))
    class Meta:
        model = File
        fields = ['file_name','file']
        
class ClientForm(forms.ModelForm):
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control client'}))
    class Meta:
        model = Client
        fields = ['nom']
        
class BeneficiaireForm(forms.ModelForm):
    CN = forms.IntegerField(label="CN", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    prenom = forms.CharField(label="Prenom", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    phone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    adresse = forms.CharField(label="Adresse", widget=forms.TextInput(attrs={'class': 'form-control beneficiaire'}))
    datenaissance = forms.DateField(label="DateNaissance", widget=forms.DateInput(attrs={'class': 'form-control datepicker_input beneficiaire'}))
    genre = forms.ChoiceField(choices = GENRE_CHOICES, label="Genre", initial='', widget=forms.Select(attrs={'class': 'form-select beneficiaire' 'input', 'id': 'selection'}), required=True)
    client = forms.ModelChoiceField(queryset=Client.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select beneficiaire' 'input', 'id': 'selection'}))
    class Meta:
        model = Beneficiaire
        fields = ['CN','nom','prenom','email','phone','adresse','datenaissance','genre','client']
        
class FormationForm(forms.ModelForm):
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control formation'}))
    theme = forms.ModelChoiceField(queryset=Theme.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select formation' 'input', 'id': 'selection_theme'}))
    formateur = forms.ModelChoiceField(queryset=Formateur.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select formation' 'input', 'id': 'selection_formateur'}))     
    client = forms.ModelChoiceField(queryset=Client.objects.all(),
                                             empty_label='',
                                             widget=forms.Select(attrs={'class': 'form-select formation' 'input', 'id': 'selection_client'}))                                         
    class Meta:
        model = Formation
        fields = ['nom','theme','formateur','client']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['formateur'].queryset = Formateur.objects.none()

        if 'theme' in self.data:
            try:
                theme_id = int(self.data.get('theme'))
                self.fields['formateur'].queryset = Formateur.objects.filter(theme=theme_id).order_by('nom')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['formateur'].queryset = self.instance.theme.formateur_theme_set.order_by('nom')
        
    




