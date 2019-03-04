from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from music.others.firebase_crud import *
# Create your views here.
from user_profile.forms import ProfileForm
from user_profile.models import Profile


@login_required()
def profile_view(request, user_id):
    user = User.objects.get(id=request.user.id)
    try:
        profile = Profile.objects.get(user=user)
        context = {
            'profile': profile
        }
        return render(request, 'user_profile/Profile.html', context)
    except ObjectDoesNotExist:
        return profile_edit(request)


def view_edit_form(request):
    user = User.objects.get(id=request.user.id)
    profile = None
    try:
        profile = Profile.objects.get(user=user)
        profile_form = ProfileForm(instance=profile)
    except ObjectDoesNotExist:
        profile_form = ProfileForm()
    context = {
        'form': profile_form,
    }
    return render(request, 'user_profile/Profile_edit.html', context)


def save_form(request):
    form = ProfileForm(request.POST, instance=Profile.objects.get(user=request.user))
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        avatar = request.FILES.get("profile_image")
        if avatar and avatar.content_type.__contains__('image/'): #check valid file
            if profile.avatar_path:
                delete_from_firebase(profile.avatar_path)
            img_folder = save_file_to_firebase(file=avatar, type='image', path='profile_pics/'+str(request.user.username))
            profile.avatar_url = img_folder[0]
            profile.avatar_path = img_folder[1]

        profile=form.save(commit=True)
    return HttpResponseRedirect(reverse('profile:profile_view', args=(request.user.id,)))

@login_required()
def profile_edit(request):

    if request.method == 'GET':
        return view_edit_form(request)

    elif request.method == 'POST':
        return save_form(request)
