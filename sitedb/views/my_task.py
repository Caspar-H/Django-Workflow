import requests
from django.shortcuts import render


def my_task(request):
    # business key and instance key mapping table
    url_mapping = "http://localhost:8080/engine-rest/process-instance/"
    query_param_mapping = {
        "processDefinitionKey": "RFEMEWorkflow"
    }
    r_mapping = requests.get(url_mapping, params=query_param_mapping).json()
    business_key_mapping = {}
    for item in r_mapping:
        business_key_mapping[item['id']] = item['businessKey']

    # Get site list under a certain user
    url_user_task = "http://localhost:8080/engine-rest/task"
    query_param = {
        "processDefinitionKey": "RFEMEWorkflow",
        "assignee": request.user.get_username(),
    }
    r_user_task = requests.get(url_user_task, params=query_param).json()
    num_user_task = len(r_user_task)

    # Append business key on user dict
    for item in r_user_task:
        # url_get_busi_key = "http://localhost:8080/engine-rest/process-instance/{}".format(item["processInstanceId"])
        item['businessKey'] = business_key_mapping[item['processInstanceId']]

    context = {
        "r_user_task": r_user_task,
        "num_user_task": num_user_task,
    }

    return render(request, 'sitedb/my_task.html', context=context)


def my_group_task(request):
    # business key and instance key mapping table
    url_mapping = "http://localhost:8080/engine-rest/process-instance/"
    query_param_mapping = {
        "processDefinitionKey": "RFEMEWorkflow"
    }
    r_mapping = requests.get(url_mapping, params=query_param_mapping).json()
    business_key_mapping = {}
    for item in r_mapping:
        business_key_mapping[item['id']] = item['businessKey']

    # Get group name
    url_group_name = "http://localhost:8080/engine-rest/group/"
    query_param = {
        "member": request.user.get_username()
    }
    r_group_name = requests.get(url_group_name, params=query_param).json()[0]

    # Get site list under a group
    url_group_task = "http://localhost:8080/engine-rest/task"
    query_param = {
        "processDefinitionKey": "RFEMEWorkflow",
        "candidateGroup": r_group_name['id'],
        "includeAssignedTasks": 'true'
    }
    r_group_task = requests.get(url_group_task, params=query_param).json()
    num_group_task = len(r_group_task)

    # Append business key on dict
    for item in r_group_task:
        item['businessKey'] = business_key_mapping[item['processInstanceId']]

    context = {
        "r_group_task": r_group_task,
        "num_group_task": num_group_task
    }

    return render(request, 'sitedb/my_group_task.html', context=context)
