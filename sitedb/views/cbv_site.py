import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView

from comment.models import Comment
from sitedb.forms import SiteForm
from sitedb.models import Site, SiteLogInfo


def home(request):
    if request.user.is_authenticated:
        return render(request, 'sitedb/home.html')
    return redirect('userlogin:login')


class SiteListView(ListView):
    model = Site
    context_object_name = 'site_data'
    template_name = 'sitedb/site_list.html'

    # do a filter for the query data
    def get_queryset(self):
        return Site.objects.all()

    # add more arguments to the returned context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)
        # To call site_current_percentage in Templates , {{site_current_percentage}}
        context['total_number'] = Site.objects.all().count()
        return context


class SiteDetailView(DetailView):
    model = Site
    slug_field = 'site_id'
    slug_url_kwarg = 'site_id'
    template_name = 'sitedb/site_detail.html'
    context_object_name = 'site_detail_info'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)

        # Get milestone info
        business_key = self.kwargs['site_id']
        url_task_name = "http://localhost:8080/engine-rest/task"
        query_param = {
            "processInstanceBusinessKey": business_key,
            "processDefinitionKey": "RFEMEWorkflow"
        }
        r_task_name = requests.get(url_task_name, params=query_param).json()

        # Get Candidate group
        task_num = len(r_task_name)
        context['loop_times'] = range(task_num)
        context['task_name'] = []
        context['task_url'] = []
        context['candidate_group'] = []
        candidate_group_mapping = {
            'emeteam': 'EME Team',
            'rfteam': 'RF Team'
        }
        for item in range(task_num):
            context['task_name'].append(r_task_name[item]['name'])
            context['task_url'].append(r_task_name[item]['taskDefinitionKey'])

            # Candidate Group
            url_candidate_group = "http://localhost:8080/engine-rest/task/{}/identity-links".format(
                r_task_name[item]['id'])
            r_candidate_group = requests.get(url_candidate_group).json()[0]['groupId']
            context['candidate_group'].append(candidate_group_mapping[r_candidate_group])

        # Get comments for the site
        comments = Comment.objects.filter(site__site_id=self.kwargs['site_id'])
        context['comments'] = comments

        return context


class SiteUpdateView(UpdateView):
    model = Site
    form_class = SiteForm
    slug_field = 'site_id'
    slug_url_kwarg = 'site_id'
    template_name = 'sitedb/site_update.html'

    def form_valid(self, form, **kwargs):
        """If the form is valid, save the associated model."""
        for item in form.changed_data:
            new_log = SiteLogInfo()
            new_log.log_user = self.request.user.get_username()
            new_log.log_site_id = self.kwargs['site_id']
            new_log.log_info = '{} Changed from {} to {}'. \
                format(Site._meta.get_field(item).verbose_name,
                       form.initial[item], form.cleaned_data[item])
            new_log.save()
        self.object = form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kwargs):
        context = super(SiteUpdateView, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['site_id']
        return context

    def get_success_url(self, **kwargs):
        return reverse('sitedb:site_detail_info', args=[self.kwargs['site_id']])


# Log List/Detail/Update View
class SiteLogListView(ListView):
    model = SiteLogInfo
    context_object_name = 'site_logs'
    template_name = 'sitedb/log_list.html'

    def get_queryset(self):
        return SiteLogInfo.objects.all().filter(log_site_id=self.kwargs['site_id'])

    def get_context_data(self, **kwargs):
        context = super(SiteLogListView, self).get_context_data(**kwargs)
        # To call site_current_percentage in Templates , {{site_current_percentage}}
        context['site_id'] = self.kwargs['site_id']
        return context


# Log List/Detail/Update View
class UserLogListView(ListView):
    model = SiteLogInfo
    context_object_name = 'user_logs'
    template_name = 'sitedb/log_user_list.html'

    def get_queryset(self):
        return SiteLogInfo.objects.all().filter(log_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserLogListView, self).get_context_data(**kwargs)
        # To call site_current_percentage in Templates , {{site_current_percentage}}
        context['user'] = self.request.user
        return context