from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from .forms import UserForm, ProfileForm
from .models import Profile


@method_decorator(cache_control(no_cache=True), name='dispatch')
class RegisterView(View):
    """Handles register view"""

    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        """Loads the register view if there is no logged in user"""
        user = request.user
        if user.is_authenticated:
            return redirect(reverse('mapper:index'))

        user_form = UserForm()
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        """
        Checks validity of posted data and either creates the
        new user or renders the form again with errors
        """
        # Binds POST data to the form
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user_form.save_m2m()
            login(request, new_user)
            return redirect(new_user.profile)

        # Renders the form again but filled in not valid
        return render(request, self.template_name, {'user_form': user_form})


@method_decorator(cache_control(no_cache=True, private=True), name='dispatch')
class ProfileView(LoginRequiredMixin, View):
    """Handles the user profile view. Requires user to be logged in"""

    template_name = 'users/profile.html'
    success_message = 'You have successfully updated your interests'

    def get(self, request, *args, **kwargs):
        """Shows the user his own profile or redirects to the login page"""
        authenticated_user = request.user
        user_id = kwargs['id']

        # Checks if the profile id requested exists
        user_profile = get_object_or_404(Profile, user_id=user_id)

        # Checks if user has access to requested profile
        if authenticated_user.id == user_id:
            profile_form = ProfileForm(instance=user_profile)
            return render(request, self.template_name, {'profile_form': profile_form})

        unauthenticated_url = f'{reverse("login")}?next={request.path}'
        return redirect(unauthenticated_url)

    def post(self, request, *args, **kwargs):
        """
        Handles profile form data and either updates
        profile or renders the form again with errors
        """
        authenticated_user = request.user
        user_profile = Profile.objects.get(user=authenticated_user)
        profile_form = ProfileForm(request.POST, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, self.success_message)
            return redirect(user_profile)

        return render(request, self.template_name, {'profile_form': profile_form})
