import os

import requests
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from WorkflowEngine.settings import CAMUNDA_HOST, BASE_DIR, ACTIVATION_WORKFLOW_NAME
from sitedb.models import Site, SiteActivation


def batch_claim_task(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/batch claim.xlsx')

    raw_data = pd.read_excel(file_path, 'Sheet1')

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
    return HttpResponse("sites have been claimed")


def batch_complete_task(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/batch complete.xlsx')

    raw_data = pd.read_excel(file_path, 'Sheet1')

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
    return HttpResponse("sites have been completed")


def batch_milestone_update(request):
    # read data from excel tracker
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/milestone update table.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    for index, row in raw_data.iterrows():
        site_id = row['Site ID']
        site_status = row['Site Status']
        milestone_list = []
        if site_status == 'site_list_ready':
            milestone_list = ['neighbouring_sites', 'cme_dump', 'testing_scenario', 'testing_route', 'acma_check',
                              'emeg_status', 'l1800_simulations', 'overlap_analysis',
                              'cell_list_update_based_on_simulation', 'site_power_up', 'shut_down_close_macrol700',
                              'activate_small_cell', 'pre_testing', 'collect_tx_design_info', 'allocate_id',
                              'pci_conflict', 'rf_script', 'check_rf_script', 'ran_script', 'dark_fibre_check',
                              'tx_cutover', 'apply_cr', 'rfnsa_update', 'cell_group_define', ]
        elif site_status == 'site_activation_ready':
            milestone_list = ['site_activation', 'service_verification', 'parameter_audit', 'day1_kpi_monitoring', ]
        elif site_status == 'post_activation':
            milestone_list = ['ric_checklist', 'isn_report_and_upload', 'apply_cr_for_phase2_parameters',
                              'phase2_parameters_kpi_monitoring', 'rf_script_for_phase2_parameters', 'dsa7_report', ]
        elif site_status == 'activation_completed':
            milestone_list = ['ric_checklist', 'isn_report_and_upload', 'apply_cr_for_phase2_parameters',
                              'phase2_parameters_kpi_monitoring', 'rf_script_for_phase2_parameters', 'dsa7_report', ]

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
            "taskDefinitionKey": 'site_list_ready',
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
                            "activityId": 'site_list_ready'
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

        # cancel the current milestone(site_list_ready)
        # status_json_content = {
        #     "skipCustomListeners": True,
        #     "skipIoMappings": True,
        #     "instructions": [
        #         {
        #             "type": 'cancel',
        #             "activityId": 'site_list_ready'
        #         }
        #     ],
        #     "annotation": "Status Initialization."
        # }
        # r_modify_milestone = requests.post(url_modify_milestone, json=status_json_content)

    return HttpResponse('Site status initialized')


def milestone_summary_activation(request):
    # filter out sites in activation project
    workflow_model_name = 'site_activation'
    workflow_status = 'activation_status'
    workflow_filter = {'site_activation__activation_plan': True}
    temp_site_list = list(Site.objects.filter(**workflow_filter))

    # list for milestones
    milestone_list_ready = ['neighbouring_sites', 'cme_dump', 'testing_scenario', 'testing_route', 'acma_check',
                            'emeg_status', 'l1800_simulations', 'overlap_analysis',
                            'cell_list_update_based_on_simulation', 'site_power_up', 'shut_down_close_macrol700',
                            'activate_small_cell', 'pre_testing', 'collect_tx_design_info', 'allocate_id',
                            'pci_conflict', 'rf_script', 'check_rf_script', 'ran_script', 'dark_fibre_check',
                            'tx_cutover', 'apply_cr', 'rfnsa_update', 'cell_group_define', ]
    milestone_activation_ready = ['site_activation', 'service_verification', 'parameter_audit', 'day1_kpi_monitoring', ]

    milestone_post_activation = ['ric_checklist', 'isn_report_and_upload', 'apply_cr_for_phase2_parameters',
                                 'phase2_parameters_kpi_monitoring', 'rf_script_for_phase2_parameters', 'dsa7_report', ]

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
        elif site_status == 'site_list_ready':
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
                    temp_site_milestone_info[task] = 'N'
                else:
                    temp_site_milestone_info[task] = 'Y'

        elif site_status == 'site_activation_ready':
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
                    temp_site_milestone_info[task] = 'N'
                else:
                    temp_site_milestone_info[task] = 'Y'

        # site in "milestone_post_activation" stage
        elif site_status == 'milestone_post_activation':
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
                    temp_site_milestone_info[task] = 'N'
                else:
                    temp_site_milestone_info[task] = 'Y'

        site_milestone_info_list.append(temp_site_milestone_info)

    table_header_list = ['Site_ID',
                         'Site Status'] + milestone_list_ready + milestone_activation_ready + milestone_post_activation
    context = {
        'site_milestone_info_list': site_milestone_info_list,
        'table_header_list': table_header_list
    }

    return render(request, 'sitedb/milestone_summary_activation_list.html', context=context)
