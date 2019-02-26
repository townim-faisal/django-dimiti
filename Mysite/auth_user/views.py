from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from .models import Profile
from .token import account_activation_token

# user sign up form
def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False) # create, but don't save the new user instance
            new_user.is_active = False
            new_user.save()
            profile = Profile(
                user = new_user,
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name')
            )
            profile.save()

            #send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Dimity Account'
            message = render_to_string('auth_user/account_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                #In Django 2.0 you should call decode() after base64 encoding the uid, to convert it to a string
                'uid': urlsafe_base64_encode(force_bytes(new_user.id)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            #print(urlsafe_base64_encode(force_bytes(new_user.id)) )
            #print(force_bytes(new_user.id))
            #print( urlsafe_base64_decode(urlsafe_base64_encode(force_bytes(new_user.id))).decode() )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            context = {'check_email': 'Please check your mail to activate', 'signup_form': UserRegistrationForm()}
            return render(request, 'auth_user/signup.html', context)
        else:
            context = {'signup_form': form}
    else:
        form = UserRegistrationForm()
        context = {'signup_form': form}
    return render(request, 'auth_user/signup.html', context)

# user sign in form
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

#user can signout
def user_signout(request):
    logout(request)
    return HttpResponseRedirect('/signin')

#user activation
def user_activate(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'auth_user/signin.html', {'activate_message' : 'Successfully activated'})
    else:
        error(request, 'Activation link is invalid!')
        return redirect('/signin')
