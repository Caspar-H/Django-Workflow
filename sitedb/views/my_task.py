import requests
from django.shortcuts import render

from WorkflowEngine.settings import CAMUNDA_HOST, ACTIVATION_WORKFLOW_NAME


def my_task(request):
    # business key and instance key mapping table
    url_mapping = "{}/process-instance/".format(CAMUNDA_HOST)
    query_param_mapping = {
        "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
    }
    r_mapping = requests.get(url_mapping, params=query_param_mapping).json()
    business_key_mapping = {}
    for item in r_mapping:
        business_key_mapping[item['id']] = item['businessKey']

    # Get site list under a certain user
    url_user_task = "{}/task".format(CAMUNDA_HOST)
    query_param = {
        "processDefinitionKey": ACTIVATION_WORKFLOW_NAME,
        "assignee": request.user.get_username(),
    }
    r_user_task = requests.get(url_user_task, params=query_param).json()
    num_user_task = len(r_user_task)

    # Append business key on user dict
    for item in r_user_task:
        item['businessKey'] = business_key_mapping[item['processInstanceId']]

    context = {
        "r_user_task": r_user_task,
        "num_user_task": num_user_task,
    }

    return render(request, 'sitedb/my_task.html', context=context)


def my_group_task(request):
    # business key and instance key mapping table
    url_mapping = "{}/process-instance/".format(CAMUNDA_HOST)
    query_param_mapping = {
        "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
    }
    r_mapping = requests.get(url_mapping, params=query_param_mapping).json()
    business_key_mapping = {}
    for item in r_mapping:
        business_key_mapping[item['id']] = item['businessKey']

    # Get group name
    url_group_name = "{}/group/".format(CAMUNDA_HOST)
    query_param = {
        "member": request.user.get_username()
    }
    r_group_name = requests.get(url_group_name, params=query_param).json()[0]
    print(r_group_name)

    # Get site list under a group
    url_group_task = "{}/task".format(CAMUNDA_HOST)
    query_param = {
        "processDefinitionKey": ACTIVATION_WORKFLOW_NAME,
        "candidateGroup": r_group_name['id'],
        "includeAssignedTasks": 'true'
    }
    r_group_task = requests.get(url_group_task, params=query_param).json()
    num_group_task = len(r_group_task)

    # Append business key on dict
    for item in r_group_task:
        item['businessKey'] = business_key_mapping[item['processInstanceId']]

    # Group member performance
    url_user_list = "{}/user".format(CAMUNDA_HOST)
    query_param = {
        'memberOfGroup': r_group_name['id']
    }
    r_user_list = requests.get(url_user_list, params=query_param).json()
    user_list = [i['id'] for i in r_user_list]
    user_count = []
    for user_name in user_list:
        # Get site list under a certain user
        url_user_task = "{}/task".format(CAMUNDA_HOST)
        query_param = {
            "processDefinitionKey": ACTIVATION_WORKFLOW_NAME,
            "candidateGroup": r_group_name['id'],
            "includeAssignedTasks": 'true',
            "assignee": user_name,
        }
        r_user_task = requests.get(url_user_task, params=query_param).json()
        num_user_task = len(r_user_task)
        user_count.append(num_user_task)

    if num_group_task - sum(user_count):
        user_list.append("Not assigned")
        user_count.append(num_group_task - sum(user_count))

    context = {
        "r_group_task": r_group_task,
        "num_group_task": num_group_task,
        "user_list": user_list,
        "user_count": user_count
    }

    return render(request, 'sitedb/my_group_task.html', context=context)
