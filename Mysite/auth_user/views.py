from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import error

# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/music')
        else:
            context = {'signup_form': form}
    else:
        form = UserCreationForm()
        context = {'signup_form': form}
    return render(request, 'auth_user/signup.html', context)

def user_signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/music')
        else:
            error(request, 'Username or password incorrect')
            return redirect('/signin')
    return render(request, 'auth_user/signin.html')


def user_signout(request):
    logout(request)
    return HttpResponseRedirect('/signin')
