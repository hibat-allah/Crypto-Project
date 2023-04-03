from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, QueryDict
from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib import messages
from authentification.views import is_ps, is_admin
from app.forms import ThemeForm, DomaineForm, FormateurForm, FormationForm, ClientForm, BeneficiaireForm, FileForm
from app.models import Theme, Domaine, Formateur, Formation, Client, Beneficiaire, Salle, File
from calendarapp.models import Event
from app.utils import set_pagination
from django.http import FileResponse, HttpResponse, Http404
from django.conf import settings
import os
 

import csv

def download(request, path):
    # get the download path
    download_path = os.path.join(settings.MEDIA_ROOT, path)
    head_tail = os.path.split(path)
    file_name = head_tail[1]
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/file")
            response['Content-Disposition'] = 'inline; filename=' + file_name
            return response
    raise Http404
    
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        if ('.pdf' in load_template):
            filepath = os.path.join('media', load_template)
            print(filepath)
            return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        else:
            context['segment'] = load_template

            html_template = loader.get_template(load_template)
            return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

def dashboard(request):
    Total=Event.objects.all().count()
    TotalF=Formation.objects.all().count()
    Total_running=Event.objects.get_running_events().count()
    Total_upcoming=Event.objects.get_upcoming_events().count()
    Total_finished=Event.objects.get_finished_events().count()
    labels_SS = []
    labels_FF = []
    labels_CF = []
    labels_TF= []
    data_SS = []
    data_FF = []
    data_CF = []
    data_TF= []
    data_MS= []
    data_AS= []
    labels_mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Aout','Septembre','Octobre','Novembre','Décembre']
    labels_annees = ['2022','2023','2024','2025','2026']
    Janvier = 0 
    Février = 0 
    Mars = 0 
    Avril = 0 
    Mai = 0 
    Juin = 0 
    Juillet = 0
    Aout = 0 
    Septembre = 0 
    Octobre = 0 
    Novembre = 0 
    Décembre = 0
    A2022=0
    A2023=0
    A2024=0
    A2025=0
    A2026=0

    salles = Salle.objects.all()
    formations = Formation.objects.all()
    formateurs = Formateur.objects.all()
    clients = Client.objects.all()
    themes = Theme.objects.all()
    domaines = Domaine.objects.all()
    for salle in salles:
        labels_SS.append('Salle '+str(salle.id))
        data_SS.append(Event.objects.filter(salle__id=salle.id).count())
    for formateur in formateurs:
        labels_FF.append('Formateur '+str(formateur.id)+' : '+formateur.nom+' '+formateur.prenom)
        data_FF.append(Formation.objects.filter(formateur__id=formateur.id).count())
    for client in clients:
        labels_CF.append('Client '+str(client.id)+' : '+client.nom)
        data_CF.append(Formation.objects.filter(client__id=client.id).count())
    for theme in themes:
        labels_TF.append('theme '+str(theme.id)+' : '+theme.nom)
        data_TF.append(Formation.objects.filter(theme__id=theme.id).count())
    events=Event.objects.all()
    for event in events:
        if(event.start_time.month == 1):
            Janvier = Janvier +1
        if(event.start_time.month == 2):
            Février = Février +1 
        if(event.start_time.month == 3):
            Mars = Mars +1 
        if(event.start_time.month == 4):
            Avril = Avril +1 
        if(event.start_time.month == 5):    
            Mai = Mai +1 
        if(event.start_time.month == 6):
            Juin = Juin +1 
        if(event.start_time.month == 7):
            Juillet = Juillet +1 
        if(event.start_time.month == 8):
            Aout = Aout +1 
        if(event.start_time.month == 9):
            Septembre = Septembre +1 
        if(event.start_time.month == 10):
            Octobre = Octobre +1 
        if(event.start_time.month == 11):
            Novembre = Novembre +1
        if(event.start_time.month == 12):
            Décembre = Décembre +1
    data_MS.append(Janvier)
    data_MS.append(Février)
    data_MS.append(Mars)
    data_MS.append(Avril)
    data_MS.append(Mai)
    data_MS.append(Juin)
    data_MS.append(Juillet)
    data_MS.append(Aout)
    data_MS.append(Septembre)
    data_MS.append(Octobre)
    data_MS.append(Novembre)
    data_MS.append(Décembre)
    events=Event.objects.all()
    for event in events:
        if(event.start_time.year == 2022):
            A2022 = A2022 +1
        if(event.start_time.month == 2023):
            A2023 = A2023 +1 
        if(event.start_time.month == 2024):
            A2024 = A2024 +1 
        if(event.start_time.month == 2025):
            A2025 = A2025 +1 
        if(event.start_time.month == 2026):    
            A2026 = A2026 +1 
    data_AS.append(A2022)
    data_AS.append(A2023)
    data_AS.append(A2024)
    data_AS.append(A2025)
    data_AS.append(A2026)
    if(is_ps(request.user)): return render(request, 'app/doc/dashboard_ps.html', {
        'Total': Total,
        'Total_running': Total_running,
        'Total_upcoming': Total_upcoming,
        'Total_finished': Total_finished,
        'data_SS': data_SS,
        'labels_SS': labels_SS,
        'data_FF': data_FF,
        'labels_FF': labels_FF,
        'data_CF': data_CF,
        'labels_CF': labels_CF,
        'data_TF': data_TF,
        'labels_TF': labels_TF,
        'labels_mois': labels_mois,
        'data_MS': data_MS,
        'data_AS': data_AS,
        'labels_annees': labels_annees
    })
    else:
        return render(request, 'page-500.html')
        
def load_formateurs(request):
    theme_id = request.GET.get('theme')
    if (theme_id == ''):
        formateurs = Formateur.objects.none()
    else:
        formateurs = Formateur.objects.filter(theme=theme_id).order_by('nom')
    return render(request, 'app/formateur_dropdown_list_options.html', {'formateurs': formateurs})
    
def load_theme(request):
    beneficiaire_id = request.GET.get('beneficiaire')
    beneficiaires = Beneficiaire.objects.filter(CN=beneficiaire_id)
    for ben in beneficiaires:
        cl = ben.client
    formations = Formation.objects.filter(client=cl.id).order_by('nom')
    return render(request, 'app/theme_dropdown_list_options.html', {'formations': formations}) 
def load_beneficiaires(request):
    beneficiaire_id = request.GET.get('beneficiaire')
    beneficiaires = Beneficiaire.objects.filter(CN=beneficiaire_id)
    for ben in beneficiaires:
        cl = ben.client
    formations = Formation.objects.filter(client=cl.id).order_by('nom')
    return render(request, 'app/theme_dropdown_list_options.html', {'formations': formations})    

def load_formateurs_bis(request):
    beneficiaire_id = request.GET.get('beneficiaire')
    beneficiaires = Beneficiaire.objects.filter(CN=beneficiaire_id)
    for ben in beneficiaires:
        cl = ben.client
    formations = Formation.objects.filter(client=cl.id).order_by('nom')
    return render(request, 'app/formateur_bis_dropdown_list_options.html', {'formations': formations})         
        
        
def create_domaine(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = DomaineForm(request.POST)
        if form.is_valid():
            form.save()
            
            msg     = 'Domaine crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('domaines'))
            
           
        else:
            msg     = 'Domaine non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = DomaineForm()

    return render(request, "app/domaines/create.html", {"form": form, "msg" : msg, "success" : success })
def create_theme(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = ThemeForm(request.POST)
        if form.is_valid():
            form.save()
            
            msg     = 'Theme crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('themes'))
            
           
        else:
            msg     = 'Theme non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = ThemeForm()

    return render(request, "app/themes/create.html", {"form": form, "msg" : msg, "success" : success })
def create_client(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            
            msg     = 'Client crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('clients'))
            
           
        else:
            msg     = 'Client non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = ClientForm()

    return render(request, "app/clients/create.html", {"form": form, "msg" : msg, "success" : success })
def create_beneficiaire(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = BeneficiaireForm(request.POST)
        if form.is_valid():
            form.save()
            
            msg     = 'Beneficiaire crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('beneficiaires'))
            
           
        else:
            msg     = 'Beneficiaire non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = BeneficiaireForm()

    return render(request, "app/beneficiaires/create.html", {"form": form, "msg" : msg, "success" : success })
def create_formateur(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = FormateurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            msg     = 'Formateur crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('formateurs'))
            
           
        else:
            msg     = 'Formateur non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = FormateurForm()

    return render(request, "app/formateurs/create.html", {"form": form, "msg" : msg, "success" : success })
def create_file(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            msg     = 'File uploadé avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('files'))
            
           
        else:
            msg     = 'File non uploadé ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = FileForm()

    return render(request, "app/files/create.html", {"form": form, "msg" : msg, "success" : success })    
def create_formation(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            
            msg     = 'Formation crée avec succes.'
            success = True
            messages.success(request, msg)
            return redirect(reverse('formations'))
            
           
        else:
            msg     = 'Formation non crée ! veuillez réessayer.'
            success = False
            messages.success(request, msg)
    else:
        form = FormationForm()

    return render(request, "app/formations/create.html", {"form": form, "msg" : msg, "success" : success })
    
def exportcsv_domaines(request):
    domaines = Domaine.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=domaines.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Code', 'Nom'])
    doms = domaines.values_list('id','code', 'nom')
    for dom in doms:
        writer.writerow(dom)
    return response
def exportcsv_themes(request):
    themes = Theme.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=themes.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom', 'Domaine'])
    thms = themes.values_list('id','nom', 'domaine__nom')
    for thm in thms:
        writer.writerow(thm)
    return response
def exportcsv_formations(request):
    formations = Formation.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=formations.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom', 'Formateur', 'Client', 'Theme'])
    foms = formations.values_list('id','nom', 'formateur__nom', 'client__nom', 'theme__nom')
    for fom in foms:
        writer.writerow(fom)
    return response
def exportcsv_formateurs(request):
    formateurs = Formateur.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=formateurs.csv'
    writer = csv.writer(response)
    writer.writerow(['CN', 'Nom', 'Prenom', 'Date de naissance', 'Genre', 'Adresse', 'Theme'])
    ftrs = formateurs.values_list('CN', 'nom', 'prenom', 'datenaissance', 'genre', 'adresse', 'theme__nom')
    for ftr in ftrs:
        writer.writerow(ftr)
    return response
def exportcsv_files(request):
    files = File.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=files.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom'])
    ftrs = files.values_list('ID', 'file_name')
    for ftr in ftrs:
        writer.writerow(ftr)
    return response    
def exportcsv_clients(request):
    clients = Client.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=clients.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Code', 'Nom'])
    clis = clients.values_list('id','code', 'nom')
    for cli in clis:
        writer.writerow(cli)
    return response
def exportcsv_beneficiaires(request):
    beneficiaires = Beneficiaire.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=beneficiaires.csv'
    writer = csv.writer(response)
    writer.writerow(['CN', 'Nom', 'Prenom', 'Date de naissance', 'Genre', 'Adresse', 'Client'])
    bens = beneficiaires.values_list('CN', 'nom', 'prenom', 'datenaissance', 'genre', 'adresse', 'client__nom')
    for ben in bens:
        writer.writerow(ben)
    return response 
    
class FormateurView(View):
    context = {'segment': 'formateurs'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)
        
    
    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('formateurs')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})
    

    def delete(self, request, pk, action=None):
        formateur = self.get_object(pk)
        formateur.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('formateurs')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()) | Q(prenom__icontains=key.strip()) | Q(theme__nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()) | Q(prenom__icontains=key.strip()) | Q(theme__nom__icontains=key.strip()))
        if filter_params :
        
            formateurs = Formateur.objects.filter(filter_params)
            if formateurs.count() == 0 : 
                formateurs = Formateur.objects.all()
                messages.warning(request, 'Element non trouvé')
        else:
            formateurs = Formateur.objects.all()
        

        self.context['formateurs'], self.context['info'] = set_pagination(request, formateurs)
        if not self.context['formateurs']:
            return False, self.context['info']

        return self.context, 'app/formateurs/list.html'
   
    def edit(self, request, pk):
        formateur = self.get_object(pk)
        self.context['formateur'] = formateur
        self.context['form'] = FormateurForm(instance=formateur)

        return self.context, 'app/formateurs/edit.html'
   

    """ Get Ajax pages """

    def edit_row(self, pk):
        formateur = self.get_object(pk)
        form = FormateurForm(instance=formateur)
        context = {'instance': formateur, 'form': form}
        return render_to_string('app/formateurs/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        formateur = get_object_or_404(Formateur, id=pk)
        return formateur

    def get_row_item(self, pk):
        formateur = self.get_object(pk)
        edit_row = render_to_string('app/formateurs/edit_row.html', {'instance': formateur})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        formateur = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = FormateurForm(form_data, instance=formateur)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Formateur sauvegardé avec succes')

            return True, 'Formateur sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'
        
class FileView(View):
    context = {'segment': 'files'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})
        if pk and action == 'download':
            template = self.download(request, pk)
        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)
        
    
    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('files')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})
    
    # def download(self, request, pk, action=None):
        # file = self.get_object(pk)
        # file_path = os.path.join(settings.MEDIA_ROOT, file.file_name)
        # print(file_path)
        # with open(file_path, 'rb') as fh:
            # response = HttpResponse(fh.read(), content_type="application/octet-stream")
            # response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            # return response

    def delete(self, request, pk, action=None):
        file = self.get_object(pk)
        file.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('files')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(file_name__icontains=key.strip()))
                    else:
                        filter_params |= (Q(file_name__icontains=key.strip()))
        if filter_params :
        
            files = File.objects.filter(filter_params)
            if files.count() == 0 : 
                files = File.objects.all()
                messages.warning(request, 'Element non trouvé')
        else:
            files = File.objects.all()
        

        self.context['files'], self.context['info'] = set_pagination(request, files)
        if not self.context['files']:
            return False, self.context['info']

        return self.context, 'app/files/list.html'
   
    def edit(self, request, pk):
        file = self.get_object(pk)
        self.context['file'] = file
        self.context['form'] = FileForm(instance=file)

        return self.context, 'app/files/edit.html'
   

    """ Get Ajax pages """

    def edit_row(self, pk):
        file = self.get_object(pk)
        form = FileForm(instance=file)
        context = {'instance': file, 'form': form}
        return render_to_string('app/files/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        file = get_object_or_404(File, id=pk)
        return file

    def get_row_item(self, pk):
        file = self.get_object(pk)
        edit_row = render_to_string('app/files/edit_row.html', {'instance': file})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        file = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = FileForm(form_data, instance=file)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'File sauvegardé avec succes')

            return True, 'File sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'
        
        
class DomaineView(View):
    context = {'segment': 'domaines'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('domaines')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        domaine = self.get_object(pk)
        domaine.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('domaines')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        val = 1
        domaines = Domaine.objects.all()
        for domaine in domaines:
            domaine.set_code('DO_'+str(val))
            domaine.save()
            val=val+1
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()))
        if filter_params :
        
            domaines = Domaine.objects.filter(filter_params)
            if domaines.count() == 0 :
                domaines = Domaine.objects.all()
                messages.warning(request, 'Element non trouvé')   
        else:
            domaines = Domaine.objects.all()

        self.context['domaines'], self.context['info'] = set_pagination(request, domaines)
        if not self.context['domaines']:
            return False, self.context['info']

        return self.context, 'app/domaines/list.html'

    def edit(self, request, pk):
        domaine = self.get_object(pk)
        self.context['domaine'] = domaine
        self.context['form'] = DomaineForm(instance=domaine)

        return self.context, 'app/domaines/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        domaine = self.get_object(pk)
        form = DomaineForm(instance=domaine)
        context = {'instance': domaine, 'form': form}
        return render_to_string('app/domaines/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        domaine = get_object_or_404(Domaine, id=pk)
        return domaine

    def get_row_item(self, pk):
        domaine = self.get_object(pk)
        edit_row = render_to_string('app/domaines/edit_row.html', {'instance': domaine})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        domaine = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = DomaineForm(form_data, instance=domaine)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Element sauvegardé avec succes')

            return True, 'Element sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'


class ThemeView(View):
    context = {'segment': 'themes'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('themes')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        theme = self.get_object(pk)
        theme.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('themes')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        val = 1
        themes = Theme.objects.all()
        for theme in themes:
            theme.set_code('TH_'+str(val))
            theme.save()
            val=val+1
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()) | Q(domaine__nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()) | Q(domaine__nom__icontains=key.strip()))
        if filter_params :
        
            themes = Theme.objects.filter(filter_params)
            if themes.count() == 0 :
                themes = Theme.objects.all()
                messages.warning(request, 'Element non trouvé')
        else:
            themes = Theme.objects.all()

        self.context['themes'], self.context['info'] = set_pagination(request, themes)
        if not self.context['themes']:
            return False, self.context['info']

        return self.context, 'app/themes/list.html'

    def edit(self, request, pk):
        theme = self.get_object(pk)
        self.context['theme'] = theme
        self.context['form'] = ThemeForm(instance=theme)

        return self.context, 'app/themes/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        theme = self.get_object(pk)
        form = ThemeForm(instance=theme)
        context = {'instance': theme, 'form': form}
        return render_to_string('app/themes/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        theme = get_object_or_404(Theme, id=pk)
        return theme

    def get_row_item(self, pk):
        theme = self.get_object(pk)
        edit_row = render_to_string('app/themes/edit_row.html', {'instance': theme})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        theme = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = ThemeForm(form_data, instance=theme)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Theme sauvegardé avec succes')

            return True, 'Theme sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'
        
       
class FormationView(View):
    context = {'segment': 'formations'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('formations')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        formation = self.get_object(pk)
        formation.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('formations')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        val = 1
        formations = Formation.objects.all()
        for formation in formations:
            formation.set_code('FO_'+str(val))
            formation.save()
            val=val+1
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()) | Q(client__nom__icontains=key.strip()) | Q(formateur__nom__icontains=key.strip()) | Q(theme__nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()) | Q(client__nom__icontains=key.strip()) | Q(formateur__nom__icontains=key.strip()) | Q(theme__nom__icontains=key.strip()))
        if filter_params :
        
            formations = Formation.objects.filter(filter_params)
            if formations.count() == 0:
                formations = Formation.objects.all()
                messages.warning(request, 'Element non trouvé')   
        else:
            formations = Formation.objects.all()


        self.context['formations'], self.context['info'] = set_pagination(request, formations)
        if not self.context['formations']:
            return False, self.context['info']

        return self.context, 'app/formations/list.html'

    def edit(self, request, pk):
        formation = self.get_object(pk)
        self.context['formation'] = formation
        self.context['form'] = FormationForm(instance=formation)

        return self.context, 'app/formations/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        formation = self.get_object(pk)
        form = FormationForm(instance=formation)
        context = {'instance': formation, 'form': form}
        return render_to_string('app/formations/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        formation = get_object_or_404(Formation, id=pk)
        return formation

    def get_row_item(self, pk):
        formation = self.get_object(pk)
        edit_row = render_to_string('app/formations/edit_row.html', {'instance': formation})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        formation = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = FormationForm(form_data, instance=formation)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Formation sauvegardé avec succes')

            return True, 'Formation sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'
        
        
class BeneficiaireView(View):
    context = {'segment': 'beneficiaires'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('beneficiaires')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        beneficiaire = self.get_object(pk)
        beneficiaire.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('beneficiaires')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):

        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()) | Q(prenom__icontains=key.strip()) | Q(client__nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()) | Q(prenom__icontains=key.strip()) | Q(client__nom__icontains=key.strip()))
        if filter_params :
        
            beneficiaires = Beneficiaire.objects.filter(filter_params) 
            if beneficiaires.count() == 0 :
                beneficiaires = Beneficiaire.objects.all()
                messages.warning(request, 'Element non trouvé')
        else:
            beneficiaires = Beneficiaire.objects.all()

        self.context['beneficiaires'], self.context['info'] = set_pagination(request, beneficiaires)
        if not self.context['beneficiaires']:
            return False, self.context['info']

        return self.context, 'app/beneficiaires/list.html'

    def edit(self, request, pk):
        beneficiaire = self.get_object(pk)
        self.context['beneficiaire'] = beneficiaire
        self.context['form'] = BeneficiaireForm(instance=beneficiaire)

        return self.context, 'app/beneficiaires/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        beneficiaire = self.get_object(pk)
        form = BeneficiaireForm(instance=beneficiaire)
        context = {'instance': beneficiaire, 'form': form}
        return render_to_string('app/beneficiaires/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        beneficiaire = get_object_or_404(Beneficiaire, id=pk)
        return beneficiaire

    def get_row_item(self, pk):
        beneficiaire = self.get_object(pk)
        edit_row = render_to_string('app/beneficiaires/edit_row.html', {'instance': beneficiaire})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        beneficiaire = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = BeneficiaireForm(form_data, instance=beneficiaire)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Beneficiaire sauvegardé avec succes')

            return True, 'Beneficiaire sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'


class ClientView(View):
    context = {'segment': 'clients'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            if pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            context, template = self.edit(request, pk)
        else:
            context, template = self.list(request)

        if not context:
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        self.update_instance(request, pk)
        return redirect('clients')

    def put(self, request, pk, action=None):
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        client = self.get_object(pk)
        client.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Element supprimé avec succes')
            redirect_url = reverse('clients')

        response = {'valid': 'success', 'message': 'Element supprimé avec succes', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        val = 1
        clients = Client.objects.all()
        for client in clients:
            client.set_code('CL_'+str(val))
            client.save()
            val=val+1
        filter_params = None
        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = (Q(nom__icontains=key.strip()))
                    else:
                        filter_params |= (Q(nom__icontains=key.strip()))
        if filter_params :
        
            clients = Client.objects.filter(filter_params)  
            if clients.count() == 0 :
                clients = Client.objects.all()
                messages.warning(request, 'Element non trouvé')
        else:
            clients = Client.objects.all()

        self.context['clients'], self.context['info'] = set_pagination(request, clients)
        if not self.context['clients']:
            return False, self.context['info']

        return self.context, 'app/clients/list.html'

    def edit(self, request, pk):
        client = self.get_object(pk)
        self.context['client'] = client
        self.context['form'] = ClientForm(instance=client)

        return self.context, 'app/clients/edit.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        client = self.get_object(pk)
        form = ClientForm(instance=client)
        context = {'instance': client, 'form': form}
        return render_to_string('app/clients/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        client = get_object_or_404(Client, id=pk)
        return client

    def get_row_item(self, pk):
        client = self.get_object(pk)
        edit_row = render_to_string('app/clients/edit_row.html', {'instance': client})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        client = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = ClientForm(form_data, instance=client)
        if form.is_valid():
            form.save()
            if not is_urlencode:
                messages.success(request, 'Client sauvegardé avec succes')

            return True, 'Client sauvegardé avec succes'

        if not is_urlencode:
            messages.warning(request, 'Erreur ! veuillez réessayer.')
        return False, 'Erreur ! veuillez réessayer.'
