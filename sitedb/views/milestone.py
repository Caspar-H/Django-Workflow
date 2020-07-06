import requests
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from notifications.signals import notify

from sitedb.models import SiteLogInfo, Site

import pandas as pd

from userlogin.models import User


def milestone_task(request, task_name, site_id):
    # Get milestone info
    url_task = "http://localhost:8080/engine-rest/task"
    query_param = {
        "processInstanceBusinessKey": site_id,
        "taskDefinitionKey": task_name,
        "processDefinitionKey": "RFEMEWorkflow"
    }
    r_task = requests.get(url_task, params=query_param).json()[0]

    return render(request, 'sitedb/milestone_task.html', locals())


def claim_task(request, task_name, site_id, ins_id):
    # Get instance id of the site
    url_claim = "http://localhost:8080/engine-rest/task/{}/claim".format(ins_id)
    json_content = {
        "userId": request.user.get_username()
    }
    r_claim = requests.post(url_claim, json=json_content)

    # # Set follow-up date
    # # Get task id
    # url_task = "http://localhost:8080/engine-rest/task"
    # query_param = {
    #     "processInstanceBusinessKey": site_id,
    #     "taskDefinitionKey": task_name,
    #     "processDefinitionKey": "RFEMEWorkflow"
    # }
    # r_task = requests.get(url_task, params=query_param).json()[0]

    # url_followup_date = "http://localhost:8080/engine-rest/task/{}".format(r_task['id'])
    # json_content = {"followUp" : timezone.now()}
    # r_followup_date = requests.put(url_followup_date, json=json_content)

    new_log = SiteLogInfo()
    new_log.log_user = request.user.get_username()
    new_log.log_site_id = site_id
    new_log.log_info = 'Task {} claimed'.format(task_name)
    new_log.save()

    notify.send(
        request.user,
        recipient=request.user,
        verb="assigned",
        target=Site.objects.get(site_id=site_id),
        description=task_name,
    )

    messages.success(request, "Task {} was claimed successfully.".format(task_name))

    return HttpResponseRedirect(reverse('sitedb:milestone_task', kwargs={'task_name': task_name, 'site_id': site_id}))


def assign_task(request, task_name, site_id, ins_id):
    if request.method == 'GET':
        # Get milestone info
        url_task = "http://localhost:8080/engine-rest/task"
        query_param = {
            "processInstanceBusinessKey": site_id,
            "taskDefinitionKey": task_name,
            "processDefinitionKey": "RFEMEWorkflow"
        }
        r_task = requests.get(url_task, params=query_param).json()[0]

        team_list = ['rfteam', 'emeteam']
        user_list = []
        for team_name in team_list:
            url_user_list = "http://localhost:8080/engine-rest/user"
            query_param = {
                'memberOfGroup': team_name
            }
            r_user_list = requests.get(url_user_list, params=query_param).json()
            user_name = [i['id'] for i in r_user_list]
            user_list += user_name

        return render(request, 'sitedb/assign_task.html', locals())

    elif request.method == 'POST':

        assignee_name = request.POST.get('assignee')

        # Get milestone info
        url_task = "http://localhost:8080/engine-rest/task"
        query_param = {
            "processInstanceBusinessKey": site_id,
            "taskDefinitionKey": task_name,
            "processDefinitionKey": "RFEMEWorkflow"
        }
        r_task = requests.get(url_task, params=query_param).json()[0]

        url_assign_task = "http://localhost:8080/engine-rest/task/{}/assignee".format(r_task['id'])
        json_content = {"userId": assignee_name}
        r_assign_task = requests.post(url_assign_task, json=json_content)

        # # Set follow-up date
        # url_followup_date = "http://localhost:8080/engine-rest/task/{}".format(r_task['id'])
        # json_content = {"followUp": timezone.now()}
        # r_followup_date = requests.put(url_followup_date, json=json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = site_id
        new_log.log_info = 'Task {} assigned to {}'.format(task_name, assignee_name)
        new_log.save()

        notify.send(
            request.user,
            recipient=User.objects.get(username=assignee_name),
            verb="assigned",
            target=Site.objects.get(site_id=site_id),
            description=task_name,
        )

        send_mail(
            'New Task Assignment',
            'You have been assigned a task by {}.'.format(request.user),
            'smtp.caspar@gmail.com',
            [User.objects.get(username=assignee_name).email],
            fail_silently=True,
        )

        messages.success(request, "Task {} was claimed successfully.".format(task_name))

        return HttpResponseRedirect(
            reverse('sitedb:milestone_task', kwargs={'task_name': task_name, 'site_id': site_id}))

    else:
        return HttpResponse("Only POST or GET request is accepted")


def unclaim_task(request, task_name, site_id, ins_id):
    url_claim = "http://localhost:8080/engine-rest/task/{}/unclaim".format(ins_id)

    r_unclaim = requests.post(url_claim)

    new_log = SiteLogInfo()
    new_log.log_user = request.user.get_username()
    new_log.log_site_id = site_id
    new_log.log_info = 'Task {} unclaimed'.format(task_name)
    new_log.save()

    messages.success(request, "Task {} was unclaimed successfully.".format(task_name))

    return HttpResponseRedirect(reverse('sitedb:milestone_task', kwargs={'task_name': task_name, 'site_id': site_id}))


def complete_task(request, task_name, site_id, ins_id):
    url_claim = "http://localhost:8080/engine-rest/task/{}/complete".format(ins_id)

    r_complete = requests.post(url_claim, headers={'Content-Type': 'application/json'})

    new_log = SiteLogInfo()
    new_log.log_user = request.user.get_username()
    new_log.log_site_id = site_id
    new_log.log_info = 'Task {} completed'.format(task_name)
    new_log.save()

    messages.success(request, "Task {} was completed successfully.".format(task_name))

    return HttpResponseRedirect(reverse('sitedb:site_detail_info', kwargs={'site_id': site_id}))


def milestone_overview(request):
    team_dict = {'rfteam': 'RF Team', 'emeteam': 'EME Team'}
    task_count_dict = {}
    # Get RF team tasks
    for key, value in team_dict.items():
        url_task = "http://localhost:8080/engine-rest/task"
        query_param = {
            "processDefinitionKey": "RFEMEWorkflow",
            "candidateGroup": key,
            "includeAssignedTasks": 'true'
        }
        r_task = requests.get(url_task, params=query_param).json()

        task_df = pd.DataFrame(r_task)
        task_count = task_df[['id', 'taskDefinitionKey', 'name']].groupby(['name', 'taskDefinitionKey']).agg(
            'count').reset_index(drop=False).values.tolist()
        task_count_dict[key] = task_count

    for i in range(len(task_count_dict['rfteam'])):
        if 'Site Completed' in task_count_dict['rfteam'][i]:
            site_completed = task_count_dict['rfteam'].pop(i)

    # List for RF team bar chart
    rf_milestone_legend = [i[0] for i in task_count_dict['rfteam']]
    rf_milestone_count = [i[2] for i in task_count_dict['rfteam']]

    # List for EME team barchat
    eme_milestone_legend = [i[0] for i in task_count_dict['emeteam']]
    eme_milestone_count = [i[2] for i in task_count_dict['emeteam']]

    context = {
        'task_count_dict': task_count_dict,
        'site_completed': site_completed,
        'rf_milestone_legend': rf_milestone_legend,
        'rf_milestone_count': rf_milestone_count,
        'eme_milestone_legend': eme_milestone_legend,
        'eme_milestone_count': eme_milestone_count,
    }
    return render(request, 'sitedb/milestone_overview.html', context=context)


def milestone_detail(request, milestone_name):
    # business key and instance key mapping table
    url_mapping = "http://localhost:8080/engine-rest/process-instance/"
    query_param_mapping = {
        "processDefinitionKey": "RFEMEWorkflow"
    }
    r_mapping = requests.get(url_mapping, params=query_param_mapping).json()
    business_key_mapping = {}
    for item in r_mapping:
        business_key_mapping[item['id']] = item['businessKey']

    # Get site list under a milestone
    url_milestone_task = "http://localhost:8080/engine-rest/task"
    query_param = {
        "processDefinitionKey": "RFEMEWorkflow",
        "taskDefinitionKey": milestone_name
    }
    r_milestone_task = requests.get(url_milestone_task, params=query_param).json()
    num_milestone_task = len(r_milestone_task)

    # Append business key on dict
    for item in r_milestone_task:
        item['businessKey'] = business_key_mapping[item['processInstanceId']]

    context = {
        "r_milestone_task": r_milestone_task,
        "num_milestone_task": num_milestone_task,
        "milestone_title_name": r_milestone_task[0]['name']
    }

    return render(request, 'sitedb/milestone_detail.html', context=context)
