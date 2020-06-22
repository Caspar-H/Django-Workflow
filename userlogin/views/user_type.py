from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from userlogin.forms import RFSignUpForm
from userlogin.models import User

import requests


class RFSignUpView(CreateView):
    model = User
    form_class = RFSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'RF'
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
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('rfteam', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class EMESignUpView(CreateView):
    model = User
    form_class = RFSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'EME'
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
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('emeteam', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')


class ManagerSignUpView(CreateView):
    model = User
    form_class = RFSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Manager'
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
        url_add_group = "http://localhost:8080/engine-rest/group/{}/members/{}".format('managementteam', user.username)
        r_add_group = requests.put(url_add_group)

        return redirect('sitedb:home')
