import os
import pandas as pd
import requests

from django.http import HttpResponse

from WorkflowEngine.settings import BASE_DIR, ACTIVATION_WORKFLOW_NAME
from sitedb.models import Site, SiteActivation, SiteSwap, SiteLogInfo


def load_site_data(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/site data.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    # raw_data['acma_id'] = raw_data['acma_id'].astype('Int64')
    # raw_data = raw_data[:5]

    for index, row in raw_data.iterrows():
        new_site = Site()
        new_site.site_id = row['Site ID']
        new_site.site_name = row['Site Name']
        new_site.site_vha_id = row['VHA ID'] if not pd.isnull(row['VHA ID']) else None
        new_site.site_vha_name = row['VHA Name'] if not pd.isnull(row['VHA Name']) else None

        new_site.site_lat = row['Latitude']
        new_site.site_long = row['Longitude']
        new_site.site_state = row['State']

        new_site.site_pole_owner = row['Pole Owner'] if not pd.isnull(row['Pole Owner']) else None
        new_site.site_pole_id = row['Pole ID'] if not pd.isnull(row['Pole ID']) else None
        new_site.site_rfnsa_id = row['RFNSA ID'] if not pd.isnull(row['RFNSA ID']) else None
        new_site.site_acma_id = row['ACMA ID'] if not pd.isnull(row['ACMA ID']) else None

        new_site.save()

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = row['Site ID']

        new_log.log_operation_type = 'data_newsite_initialization'

        new_log.save()

        # Start instance in Camunda engine
        # business_key = row['site_id']
        # url_start_process = "http://localhost:8080/engine-rest/process-definition/key/SITESURVEY/start"
        # json_content = {
        #     "businessKey": business_key
        # }
        # r_start_process = requests.post(url_start_process, json=json_content)

    return HttpResponse('Data Loaded')


def init_site_status(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/test_data/status_data_new.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    for index, row in raw_data.iterrows():
        # Start workflow with Business key
        business_key = row['site_id']
        url_start_process = "http://localhost:8080/engine-rest/process-definition/key/RFEMEWorkflow/start"
        json_content = {
            "businessKey": business_key
        }
        r_start_process = requests.post(url_start_process, json=json_content)

        # Get process instance id

        process_definition_id = r_start_process.json()['id']

        # Modify status
        url_modify_milestone = 'http://localhost:8080/engine-rest/process-instance/{}/modification'.format(
            process_definition_id)
        if not pd.isna(row['second_status']):
            status_json_content = {
                "skipCustomListeners": True,
                "skipIoMappings": True,
                "instructions": [
                    {
                        "type": row['first_status_type'],
                        "activityId": row['first_status']
                    },
                    {
                        "type": row['second_status_type'],
                        "activityId": row['second_status']
                    },
                    {
                        "type": "cancel",
                        "activityId": "mslrelease"
                    }
                ],
                "annotation": "Status Initialization."
            }
        else:
            status_json_content = {
                "skipCustomListeners": True,
                "skipIoMappings": True,
                "instructions": [
                    {
                        "type": row['first_status_type'],
                        "activityId": row['first_status']
                    },
                    {
                        "type": "cancel",
                        "activityId": "mslrelease"
                    }
                ],
                "annotation": "Status Initialization."
            }
        r_modify_milestone = requests.post(url_modify_milestone, json=status_json_content)

    return HttpResponse('Status Updated')


# load activation site status

def load_site_data_activation(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/activation table.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    # raw_data['acma_id'] = raw_data['acma_id'].astype('Int64')
    # raw_data = raw_data[:5]

    for index, row in raw_data.iterrows():
        new_site = Site.objects.get(site_id=row['Site ID'])

        temp_activation = SiteActivation()
        temp_activation.site = new_site
        temp_activation.activation_plan = True
        temp_activation.activation_schedule = row['Activation Schedule']
        temp_activation.activation_status = row['Activation Status']

        temp_activation.save()

        # Start instance in Camunda engine

        business_key = row['Site ID']
        url_start_process = "http://localhost:8080/engine-rest/process-definition/key/{}/start".format(
            ACTIVATION_WORKFLOW_NAME)
        json_content = {
            "businessKey": business_key
        }
        r_start_process = requests.post(url_start_process, json=json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = row['Site ID']

        new_log.log_operation_type = 'workflow_newsite_initialization'

        new_log.save()

    return HttpResponse('Data Loaded & Site Status Initialized')


def load_site_data_swap(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/smallcell data/swap table.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    # raw_data['acma_id'] = raw_data['acma_id'].astype('Int64')
    # raw_data = raw_data[:5]

    for index, row in raw_data.iterrows():
        new_site = Site.objects.get(site_id=row['Site ID'])

        temp_swap = SiteSwap()
        temp_swap.site = new_site
        temp_swap.swap_plan = True
        temp_swap.swap_schedule = row['Swap Schedule']
        temp_swap.swap_status = row['Swap Status']

        temp_swap.save()

        # Start instance in Camunda engine
        # business_key = row['site_id']
        # url_start_process = "http://localhost:8080/engine-rest/process-definition/key/SITESURVEY/start"
        # json_content = {
        #     "businessKey": business_key
        # }
        # r_start_process = requests.post(url_start_process, json=json_content)

        new_log = SiteLogInfo()
        new_log.log_user = request.user.get_username()
        new_log.log_site_id = row['Site ID']

        new_log.log_operation_type = 'workflow_newsite_initialization'

    return HttpResponse('Data Loaded')


def delete_site_data(request):
    site_data = Site.objects.all()
    site_data.delete()

    return HttpResponse('All Site Data Deleted')
