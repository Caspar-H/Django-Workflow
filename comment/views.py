from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from comment.forms import CommentForm
from comment.models import Comment
from sitedb.models import Site


def post_comment(request, site_id):
    site = get_object_or_404(Site, site_id=site_id)
    # site = Site.objects.filter(site_id=site_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.site = site
            new_comment.user = request.user

            new_comment.save()
            return redirect(site)
        else:
            return HttpResponse('Content in form is not correct, please check.')

    else:
        return HttpResponse('Only POST request is accepted when posting comments.')


class CommentNoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'notices'
    template_name = 'comment/notice_list.html'
    login_url = '/userlogin/login/'

    def get_queryset(self):
        return self.request.user.notifications.unread()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentNoticeListView, self).get_context_data(**kwargs)
        context['read_notices'] = self.request.user.notifications.read()

        return context


class CommentNoticeUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id')
        site_id = request.GET.get('site_id')
        task_name = request.GET.get('task_name')

        if site_id:
            request.user.notifications.get(id=notice_id).mark_as_read()
            return reverse('sitedb:milestone_task', args={'task_name': task_name, 'site_id': site_id})
            # return redirect('sitedb:home')

        else:
            request.user.notifications.mark_all_as_read()
            return redirect('comment:notice_list')
