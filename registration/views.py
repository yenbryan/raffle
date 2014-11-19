import json
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import facebook
from registration.forms import ProfileUserCreationForm, PictureForm, AboutMeForm, ProfileForm
from registration.models import Profile


def register(request):
    if request.method == 'POST':
        form = ProfileUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.send_email("welcome {}".format(user.username), "Thank you for signing up")
            return redirect("login")
    else:
        form = ProfileUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })
#
#
# @login_required()
# def upload_profile_picture(request):
#     if request.method == 'POST':
#         picture_form = PictureForm(request.POST, request.FILES)
#         if picture_form.is_valid():
#             pic = ProfilePicture(description=picture_form.cleaned_data['description'],
#                           image=picture_form.cleaned_data['picture'],
#                           profile=Profile.objects.get(id=request.user.id))
#             pic.save()
#         return redirect('profile')
#
#
# @login_required()
# def dashboard(request):
#     profile = request.user
#     about_me_form = AboutMeForm(initial={'description':request.user.about_me})
#     profile_form = ProfileForm(initial={'first_name': request.user.first_name,
#                                         'last_name': request.user.last_name})
#     try:
#         profile_picture = ProfilePicture.objects.get(profile=profile, default_picture=True)
#     except:
#         profile_picture = None
#     received_messages = Receiver.objects.filter(recipient=request.user)
#     return render(request, 'profile/dashboard.html', {'dashboard': 'active',
#                                                       'profile': profile_picture,
#                                                       'received_messages': received_messages,
#                                                       'about_me_form': about_me_form,
#                                                       'profile_form': profile_form})
#
#
# #Todo still needs work
# def new_social_user_redirect(request):
#     user_social_auth = request.user.social_auth.filter(provider='facebook').first()
#     graph = facebook.GraphAPI(user_social_auth.extra_data['access_token'])
#     profile_data = graph.get_object("me")
#     picture_data = graph.get_object('me/picture')
#
#     friends = graph.get_object('me/friends')
#     return render(request, 'profile.html', {'profile':profile_data,
#                                             'picture': picture_data,
#                                             'friends': friends})
#     # return redirect('dashboard')
#
#
# @csrf_exempt
# def ajax_about_me_update(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         about_me_form = AboutMeForm(request.POST)
#         if about_me_form.is_valid():
#             Profile(about_me=about_me_form.cleaned_data['description']).save()


def account(request):
    return render(request,'registration/account.html', {})