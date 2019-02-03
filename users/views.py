from django.views import View
from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import UserForm, ProfileForm
from .models import Profile

class RegisterView(View):

    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        # Binds POST data to the form
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user_form.save_m2m()
            login(request, new_user)
            return redirect('users:profile', id=new_user.id)

        # Renders the form again but filled in not valid
        return render(request, self.template_name, {'user_form': user_form})


class ProfileView(View):

    template_name = 'users/profile.html'
    success_message = 'You have successfully updated your interests'

    def get(self, request, *args, **kwargs):
        authenticated_user = request.user

        # Checks if user has access to requested profile
        if authenticated_user.id == kwargs['id']:
            user_profile = Profile.objects.get(user=authenticated_user)
            profile_form = ProfileForm(instance=user_profile)
            return render(request, self.template_name, {'profile_form': profile_form})

        unauthenticated_url = f'{reverse("login")}?next={request.path}'
        return redirect(unauthenticated_url)

    def post(self, request, *args, **kwargs):
        authenticated_user = request.user
        user_profile = Profile.objects.get(user=authenticated_user)
        profile_form = ProfileForm(request.POST, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, self.success_message)
            return redirect('users:profile', id=authenticated_user.id,)

        return render(request, self.template_name, {'profile_form': profile_form})