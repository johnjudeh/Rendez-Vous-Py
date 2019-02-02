from django.views import View
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import UserForm, ProfileForm

class RegisterView(View):

    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        # profile_form = ProfileForm()

        # p = Profile.objects.get(pk=1)
        # profile_form = ProfileForm(instance=p)

        # return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

        user_form = UserForm()
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        # TODO: Figure out how to post two different forms from this view (either two separately posted or together)
        # Binds POST data to the form
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user_form.save_m2m()
            login(request, new_user)
            return redirect('mapper:index')

        # Renders the form again but filled in not valid
        return render(request, self.template_name, {'user_form': user_form})