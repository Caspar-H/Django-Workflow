import os

import requests
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from WorkflowEngine.settings import CAMUNDA_HOST, BASE_DIR, ACTIVATION_WORKFLOW_NAME, ACTIVATION_LIST_READY, \
    ACTIVATION_ACTIVATION_READY, ACTIVATION_POST_ACTIVATION
from sitedb.models import Site, SiteActivation, SiteLogInfo


def batch_claim_task(request, filename):
    # file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/batch claim.xlsx')
    #
    # raw_data = pd.read_excel(file_path, 'Sheet1')
    raw_data = pd.read_excel(filename)

    for index, row in raw_data.iterrows():
        site_id = row['Site ID']
        task_name = row['Task ID']
        print(site_id, task_name)
        # get task instance id
        url_task = "{}/task".format(CAMUNDA_HOST)
        query_param = {
            "processInstanceBusinessKey": site_id,
            "taskDefinitionKey": task_name,
            "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
        }
        r_task = requests.get(url_task, params=query_param).json()[0]

        ins_id = r_task['id']

        url_claim = "{}/task/{}/claim".format(CAMUNDA_HOST, ins_id)
        json_content = {
            "userId": request.user.get_username()
        }
        r_claim = requests.post(url_claim, json=json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = site_id

        if task_name in ACTIVATION_LIST_READY:
            new_log.log_major_milestone = 'pre_activation'
        elif task_name in ACTIVATION_ACTIVATION_READY:
            new_log.log_major_milestone = 'activation'
        elif task_name in ACTIVATION_POST_ACTIVATION:
            new_log.log_major_milestone = 'post_activation'

        new_log.log_sub_milestone = task_name
        new_log.log_operation_type = 'batch_claim'

        new_log.log_info = 'Task {} batch claim'.format(task_name)
        new_log.save()

    return HttpResponse("sites have been claimed")


def batch_complete_task(request, filename):
    # file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/batch complete.xlsx')
    #
    # raw_data = pd.read_excel(file_path, 'Sheet1')
    raw_data = pd.read_excel(filename)

    for index, row in raw_data.iterrows():
        site_id = row['Site ID']
        task_name = row['Task ID']
        print(site_id, task_name)
        # get task instance id
        url_task = "{}/task".format(CAMUNDA_HOST)
        query_param = {
            "processInstanceBusinessKey": site_id,
            "taskDefinitionKey": task_name,
            "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
        }
        r_task = requests.get(url_task, params=query_param).json()[0]

        ins_id = r_task['id']

        url_complete = "{}/task/{}/complete".format(CAMUNDA_HOST, ins_id)
        json_content = {
            "userId": request.user.get_username()
        }
        r_complete = requests.post(url_complete, json=json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = site_id

        if task_name in ACTIVATION_LIST_READY:
            new_log.log_major_milestone = 'pre_activation'
        elif task_name in ACTIVATION_ACTIVATION_READY:
            new_log.log_major_milestone = 'activation'
        elif task_name in ACTIVATION_POST_ACTIVATION:
            new_log.log_major_milestone = 'post_activation'

        new_log.log_sub_milestone = task_name
        new_log.log_operation_type = 'batch_complete'

        new_log.log_info = 'Task {} batch complete'.format(task_name)
        new_log.save()

    return HttpResponse("sites have been completed")


def batch_milestone_update(request):
    # read data from excel tracker
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/milestone update table.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    for index, row in raw_data.iterrows():
        site_id = row['Site ID']
        site_status = row['Site Status']
        milestone_list = []
        if site_status == 'pre_activation':
            milestone_list = ACTIVATION_LIST_READY
        elif site_status == 'activation':
            milestone_list = ACTIVATION_ACTIVATION_READY
        elif site_status == 'post_activation':
            milestone_list = ACTIVATION_POST_ACTIVATION
        elif site_status == 'activation_completed':
            milestone_list = ACTIVATION_POST_ACTIVATION

        # site status
        temp_site = Site.objects.get(site_id=site_id)
        temp_site.site_activation.activation_status = row['Site Status']
        temp_site.site_activation.save()
        # temp_activation = SiteActivation()
        # temp_activation.site = temp_site
        # temp_activation.activation_plan = True
        # temp_activation.activation_status = row['Site Status']
        # temp_activation.save()

        # Start workflow with Business key
        # business_key = site_id
        # url_start_process = "{}/process-definition/key/{}/start".format(CAMUNDA_HOST, ACTIVATION_WORKFLOW_NAME)
        # json_content = {
        #     "businessKey": business_key
        # }
        # r_start_process = requests.post(url_start_process, json=json_content)

        # get task instance id
        url_task = "{}/task".format(CAMUNDA_HOST)
        query_param = {
            "processInstanceBusinessKey": site_id,
            "taskDefinitionKey": 'pre_activation',
            "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
        }
        r_task = requests.get(url_task, params=query_param).json()[0]

        # Get process instance id
        process_definition_id = r_task['processInstanceId']
        # process_definition_id = r_start_process.json()['id']

        # Modify status
        url_modify_milestone = '{}/process-instance/{}/modification'.format(
            CAMUNDA_HOST, process_definition_id)

        for task in milestone_list:
            if row[task] == 'Y':
                status_json_content = {
                    "skipCustomListeners": True,
                    "skipIoMappings": True,
                    "instructions": [
                        {
                            "type": 'startAfterActivity',
                            "activityId": task
                        },
                        {
                            "type": 'cancel',
                            "activityId": 'pre_activation'
                        }
                    ],
                    "annotation": "Status Initialization."
                }
            elif row[task] == 'N':
                status_json_content = {
                    "skipCustomListeners": True,
                    "skipIoMappings": True,
                    "instructions": [
                        {
                            "type": 'startBeforeActivity',
                            "activityId": task
                        },
                        {
                            "type": 'cancel',
                            "activityId": 'site_list_ready'
                        }
                    ],
                    "annotation": "Status Initialization."
                }
            r_modify_milestone = requests.post(url_modify_milestone, json=status_json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = site_id

        new_log.log_operation_type = 'workflow_status_mapping'

        new_log.save()
    return HttpResponse('Site status initialized')


def milestone_summary_activation(request, submilestone_type):
    # filter out sites in activation project
    workflow_model_name = 'site_activation'
    workflow_status = 'activation_status'

    # list for milestones
    # change the milestone query list based on request
    if submilestone_type == 'all':
        milestone_list_ready = ACTIVATION_LIST_READY
        milestone_activation_ready = ACTIVATION_ACTIVATION_READY
        milestone_post_activation = ACTIVATION_POST_ACTIVATION
        workflow_filter = {'site_activation__activation_plan': True}
    elif submilestone_type == 'pre_activation':
        milestone_list_ready = ACTIVATION_LIST_READY
        milestone_activation_ready = []
        milestone_post_activation = []
        workflow_filter = {'site_activation__activation_plan': True,
                           'site_activation__activation_status': 'pre_activation'}

    elif submilestone_type == 'activation':
        milestone_list_ready = []
        milestone_activation_ready = ACTIVATION_ACTIVATION_READY
        milestone_post_activation = []
        workflow_filter = {'site_activation__activation_plan': True,
                           'site_activation__activation_status': 'activation'}

    elif submilestone_type == 'post_activation':
        milestone_list_ready = []
        milestone_activation_ready = []
        milestone_post_activation = ACTIVATION_POST_ACTIVATION
        workflow_filter = {'site_activation__activation_plan': True,
                           'site_activation__activation_status': 'post_activation'}

    # get the site list
    temp_site_list = list(Site.objects.filter(**workflow_filter))

    # query status of milestone for each of sites
    site_milestone_info_list = []
    for temp_site in temp_site_list:
        site_status = getattr(getattr(temp_site, workflow_model_name), workflow_status)
        temp_site_milestone_info = {'Site ID': temp_site.site_id, 'Site Status': site_status}

        # site in "not_started" stage
        if site_status == 'not_started':
            for task in milestone_list_ready + milestone_activation_ready + milestone_post_activation:
                temp_site_milestone_info[task] = 'N'

        # site in "site_list_ready" stage
        elif site_status == 'pre_activation':
            for task in milestone_activation_ready + milestone_post_activation:
                temp_site_milestone_info[task] = 'N'

            # query task status in Camunda
            # Get milestone info
            business_key = temp_site.site_id
            url_task_name = "{}/task".format(CAMUNDA_HOST)
            query_param = {
                "processInstanceBusinessKey": business_key,
                "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
            }
            r_task_name = requests.get(url_task_name, params=query_param).json()
            temp_task_list = [t['taskDefinitionKey'] for t in r_task_name]
            for task in milestone_list_ready:
                if task not in temp_task_list:
                    temp_site_milestone_info[task] = 'Y'
                else:
                    temp_site_milestone_info[task] = 'N'

        elif site_status == 'activation':
            for task in milestone_post_activation:
                temp_site_milestone_info[task] = 'N'
            for task in milestone_list_ready:
                temp_site_milestone_info[task] = 'Y'

            # query task status in Camunda
            # Get milestone info
            business_key = temp_site.site_id
            url_task_name = "{}/task".format(CAMUNDA_HOST)
            query_param = {
                "processInstanceBusinessKey": business_key,
                "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
            }
            r_task_name = requests.get(url_task_name, params=query_param).json()
            temp_task_list = [t['taskDefinitionKey'] for t in r_task_name]
            for task in milestone_activation_ready:
                if task not in temp_task_list:
                    temp_site_milestone_info[task] = 'Y'
                else:
                    temp_site_milestone_info[task] = 'N'

        # site in "post_activation" stage
        elif site_status == 'post_activation':
            for task in milestone_list_ready + milestone_activation_ready:
                temp_site_milestone_info[task] = 'Y'

            # query task status in Camunda
            # Get milestone info
            business_key = temp_site.site_id
            url_task_name = "{}/task".format(CAMUNDA_HOST)
            query_param = {
                "processInstanceBusinessKey": business_key,
                "processDefinitionKey": ACTIVATION_WORKFLOW_NAME
            }
            r_task_name = requests.get(url_task_name, params=query_param).json()
            temp_task_list = [t['taskDefinitionKey'] for t in r_task_name]
            for task in milestone_post_activation:
                if task not in temp_task_list:
                    temp_site_milestone_info[task] = 'Y'
                else:
                    temp_site_milestone_info[task] = 'N'

        site_milestone_info_list.append(temp_site_milestone_info)

    table_header_list = ['Site ID',
                         'Site Status'] + milestone_list_ready + milestone_activation_ready + milestone_post_activation
    context = {
        'site_milestone_info_list': site_milestone_info_list,
        'table_header_list': table_header_list,
    }

    return render(request, 'sitedb/milestone_summary_activation_list.html', context=context)


def batch_operation(request, operation_type):

    if request.method == "GET":
        return render(request, 'sitedb/batch_operation.html', locals())
    elif request.method == "POST":
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.xlsx'):
                print('File is not Excel.xlsx type')
                return HttpResponseRedirect(reverse("sitedb:batch_operation"))

            if operation_type == 'batch_claim':
                batch_claim_task(request, csv_file)
            elif operation_type == 'batch_complete':
                batch_complete_task(request, csv_file)

            # load_rfnsa_dump(csv_file)

        except Exception as e:
            print(e)
            print("Unable to complete batch operation. ")

            return render(request, 'sitedb/batch_operation_fail.html', locals())

        return render(request, 'sitedb/batch_operation_success.html', locals())