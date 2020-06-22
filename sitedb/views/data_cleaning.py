import os
import pandas as pd
import requests

from django.http import HttpResponse

from WorkflowEngine.settings import BASE_DIR
from sitedb.models import Site


def load_site_data(request):
    file_path = os.path.join(BASE_DIR, 'sitedb/test_data/test_site_data.xlsx')
    raw_data = pd.read_excel(file_path, 'Sheet1')

    raw_data['acma_id'] = raw_data['acma_id'].astype('Int64')
    # raw_data = raw_data[:5]

    for index, row in raw_data.iterrows():
        new_site = Site()
        new_site.site_id = row['site_id']
        new_site.site_name = row['site_name']
        new_site.site_lat = row['latitude']
        new_site.site_long = row['longitude']
        new_site.site_cluster = row['cluster_name']
        new_site.site_state = row['state']
        new_site.site_pole_owner = row['pole_owner']
        new_site.site_pole_id = row['pole_id']
        new_site.site_rfnsa_id = row['rfnsa_id'] if not pd.isnull(row['rfnsa_id']) else None
        new_site.site_acma_id = row['acma_id'] if not pd.isnull(row['acma_id']) else None

        new_site.save()
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
