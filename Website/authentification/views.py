from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from app.models import Theme, Formateur, Client, Beneficiaire, Formation
from django.contrib.auth import logout
# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'user/index.html')
def index_views(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'user/index.html')
    
#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_superuser : 
        logout(request)
    if request.user.is_authenticated:
        if (is_adv(request.user) or is_ps(request.user)):
            return render(request,'user/adminclick.html')
        else : 
            return HttpResponseRedirect('afterlogin')
    return render(request,'user/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def advclick_view(request):
    if request.user.is_superuser : 
        logout(request)
    if request.user.is_authenticated:
        if (is_admin(request.user) or is_ps(request.user)):
            return render(request,'user/advclick.html')
        else : 
            return HttpResponseRedirect('afterlogin')
    return render(request,'user/advclick.html')

#for showing signup/login button for patient(by sumit)
def psclick_view(request):
    if request.user.is_superuser : 
        logout(request)
    if request.user.is_authenticated:
        if (is_admin(request.user) or is_adv(request.user)):
            return render(request,'user/psclick.html')
        else : 
            return HttpResponseRedirect('afterlogin')
    return render(request,'user/psclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'user/adminsignup.html',{'form':form})

def adv_signup_view(request):
    userForm=forms.AdvUserForm()
    advForm=forms.AdvForm()
    mydict={'userForm':userForm,'advForm':advForm}
    if request.method=='POST':
        userForm=forms.AdvUserForm(request.POST)
        advForm=forms.AdvForm(request.POST,request.FILES)
        if userForm.is_valid() and advForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            adv=advForm.save(commit=False)
            adv.user=user
            adv=adv.save()
            my_adv_group = Group.objects.get_or_create(name='ADV')
            my_adv_group[0].user_set.add(user)
        return HttpResponseRedirect('advlogin')
    return render(request,'user/advsignup.html',context=mydict)


def ps_signup_view(request):
    userForm=forms.PsUserForm()
    psForm=forms.PsForm()
    mydict={'userForm':userForm,'psForm':psForm}
    if request.method=='POST':
        userForm=forms.PsUserForm(request.POST)
        psForm=forms.PsForm(request.POST,request.FILES)
        if userForm.is_valid() and psForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            ps=psForm.save(commit=False)
            ps.user=user
            ps=ps.save()
            my_ps_group = Group.objects.get_or_create(name='PS')
            my_ps_group[0].user_set.add(user)
        return HttpResponseRedirect('pslogin')
    return render(request,'user/pssignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_adv(user):
    return user.groups.filter(name='ADV').exists()
def is_ps(user):
    return user.groups.filter(name='PS').exists()





#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if request.user.is_superuser : 
        logout(request)
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_adv(request.user):
        accountapproval=models.adv.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('adv-dashboard')
        else:
            return render(request,'user/adv_wait_for_approval.html')
    elif is_ps(request.user):
        accountapproval=models.ps.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('ps-dashboard')
        else:
            return render(request,'user/ps_wait_for_approval.html')

  
    





#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    return redirect('calendarapp:calendar')


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_adv_view(request):
    return render(request,'user/admin_adv.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_adv_view(request):
    advs=models.adv.objects.all().filter(status=True)
    return render(request,'user/admin_view_adv.html',{'adv':advs})





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_adv_view(request):
    #those whose approval are needed
    advs=models.adv.objects.all().filter(status=False)
    return render(request,'user/admin_approve_adv.html',{'adv':advs})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_adv_view(request,pk):
    adv=models.adv.objects.get(id=pk)
    adv.status=True
    adv.save()
    return redirect(reverse('admin-approve-adv'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_adv_view(request,pk):
    Adv=models.adv.objects.get(id=pk)
    user=models.User.objects.get(id=Adv.user_id)
    user.delete()
    Adv.delete()
    return redirect(reverse('admin-approve-adv'))




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_ps_view(request):
    return render(request,'user/admin_ps.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_ps_view(request):
    ps=models.ps.objects.all().filter(status=True)
    return render(request,'user/admin_view_ps.html',{'ps':ps})


#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_ps_view(request):
    #those whose approval are needed
    ps=models.ps.objects.all().filter(status=False)
    return render(request,'user/admin_approve_ps.html',{'ps':ps})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_ps_view(request,pk):
    ps=models.ps.objects.get(id=pk)
    ps.status=True
    ps.save()
    return redirect(reverse('admin-approve-ps'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_ps_view(request,pk):
    Ps=models.ps.objects.get(id=pk)
    user=models.User.objects.get(id=Ps.user_id)
    user.delete()
    Ps.delete()
    return redirect(reverse('admin-approve-ps'))

def documents(request):
    Formateurs=Formateur.objects.all()
    Beneficiaires=Beneficiaire.objects.all()
    Themes=Theme.objects.all()
    Clients=Client.objects.all()
    Formations=Formation.objects.all()
    context ={
            'Formateurs':Formateurs,
            'Formations':Formations,
            'Beneficiaires':Beneficiaires,
            'Themes':Themes,
            'Clients':Clients
        }
    if(is_adv(request.user)):
        return render(request,'app/doc/Documents_adv.html',context)
    if(is_admin(request.user)):
        return render(request,'app/doc/Documents.html',context)    
    
@login_required(login_url='advlogin')
@user_passes_test(is_adv)
def adv_dashboard_view(request):
    return redirect('documents')
@login_required(login_url='pslogin')
@user_passes_test(is_ps) 
def ps_dashboard_view(request):
    return render(request,'app/doc/dashboard_ps.html')
    
