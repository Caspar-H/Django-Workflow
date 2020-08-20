from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from userlogin.forms import VHARFSignUpForm, TPGRFSignUpForm, TPGSAEDSignUpForm, TPGEMESignUpForm, \
    TPGPMSignUpForm
from userlogin.models import User

import requests


class VHARFSignUpView(CreateView):
    model = User
    form_class = VHARFSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'VHA RF'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # Create user in Camunda
        url_create_user = 'http://localhost:8080/engine-rest/user/create' # todo Use global variables to replace Camunda port
        json_data = {"profile":
                         {"id": user.username,
                          "firstName": user.first_name,
                          "lastName": user.last_name,
                          "email": user.email},
                     "credentials":
                         {"password": 'password123'}
                     }
        r_create_user = requests.post(url_create_user, json=json_data)

        # Add member to the group
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('vharf', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class TPGRFSignUpView(CreateView):
    model = User
    form_class = TPGRFSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'TPG RF'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # Create user in Camunda
        url_create_user = 'http://localhost:8080/engine-rest/user/create'
        json_data = {"profile":
                         {"id": user.username,
                          "firstName": user.first_name,
                          "lastName": user.last_name,
                          "email": user.email},
                     "credentials":
                         {"password": 'password123'}
                     }
        r_create_user = requests.post(url_create_user, json=json_data)

        # Add member to the group
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('tpgrf', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class TPGSAEDSignUpView(CreateView):
    model = User
    form_class = TPGSAEDSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'TPG SAED'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Create user in Camunda
        url_create_user = 'http://localhost:8080/engine-rest/user/create'
        json_data = {"profile":
                         {"id": user.username,
                          "firstName": user.first_name,
                          "lastName": user.last_name,
                          "email": user.email},
                     "credentials":
                         {"password": 'password123'}
                     }
        r_create_user = requests.post(url_create_user, json=json_data)

        # Add member to the group
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('tpgsaed', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class TPGEMESignUpView(CreateView):
    model = User
    form_class = TPGEMESignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'TPG EME'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Create user in Camunda
        url_create_user = 'http://localhost:8080/engine-rest/user/create'
        json_data = {"profile":
                         {"id": user.username,
                          "firstName": user.first_name,
                          "lastName": user.last_name,
                          "email": user.email},
                     "credentials":
                         {"password": 'password123'}
                     }
        r_create_user = requests.post(url_create_user, json=json_data)

        # Add member to the group
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('tpgeme', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class TPGPMSignUpView(CreateView):
    model = User
    form_class = TPGPMSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'TPG PM'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Create user in Camunda
        url_create_user = 'http://localhost:8080/engine-rest/user/create'
        json_data = {"profile":
                         {"id": user.username,
                          "firstName": user.first_name,
                          "lastName": user.last_name,
                          "email": user.email},
                     "credentials":
                         {"password": 'password123'}
                     }
        r_create_user = requests.post(url_create_user, json=json_data)

        # Add member to the group
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('tpgpm', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')