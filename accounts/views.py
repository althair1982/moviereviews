from django.shortcuts import render
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

def signupaccount(request):
    if request.method == 'GET':
        return render(request,'signupaccount.html',{'form':UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error':'Wpisana nazwa użytkownika jest już zajęta. Wybierz inną'})
        else:
            return render(request, 'signupaccount.html',
                  {'form': UserCreateForm,
                   'error': 'Hasła różnią się.'})

def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html',
                      {'form':AuthenticationForm})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request,'loginaccount.html',
                          {'form': AuthenticationForm(),
                           'error': 'Dane logowania nie są poprawne.'})
        else:
            login(request,user)
            return redirect('home')

@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


