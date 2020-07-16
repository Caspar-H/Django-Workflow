from django.http import HttpResponse
from django.shortcuts import render, redirect

from WorkflowEngine.settings import MINIO_HOST
from minio import Minio, ResponseError

import tkinter
import tkinter.messagebox as tkmb
from tkinter.filedialog import askdirectory

import os

minioClient = Minio(MINIO_HOST,
                    access_key='tpg12345',
                    secret_key='tpg12345',
                    secure=False)
bucket_name = 'siteinfo'


# Create your views here.
def documents_folder(request):
    if request.method == 'GET':
        # Get object list
        objects = minioClient.list_objects(bucket_name, prefix=request.GET.get('prefix', ''), recursive=False)

        folder_list = []
        file_list = []

        for obj in objects:
            # print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
            #       obj.etag, obj.size, obj.content_type, obj.is_dir)
            if obj.is_dir:
                folder_list.append({'folder_name': obj.object_name.split('/')[-2], 'object_name': obj.object_name})
            else:
                file_list.append({'file_name': obj.object_name.split('/')[-1], 'last_modified': obj.last_modified,
                                  'object_name': obj.object_name})
        # print(folder_list)
        # print(file_list)
        return render(request, 'fileupload/documents_folder.html', locals())
    elif request.method == 'POST':

        return render(request, 'fileupload/documents_folder.html', locals())


def documents_download(request):
    # Get a full object.
    try:
        root = tkinter.Tk()
        root.withdraw()

        path = askdirectory(title='Select Folder')  # shows dialog box and return the path

        object_name = request.GET.get('object_name')
        data = minioClient.get_object(bucket_name, object_name)

        file_path = '/'.join(object_name.split('/')[:-1])+'/'
        if file_path == '/':
            file_path = ''

        if not path:
            response = redirect('fileupload:documents_folder')
            response['Location'] += '?prefix={}'.format(file_path)
            root.destroy()
            return response

        file_dir = path + '/' + object_name.split('/')[-1]

        if os.path.isfile(file_dir):
            is_replace = tkmb.askyesno("Replace or Skip Files",
                                       "The destination already has a file named {}, do you want to replace it?".format(
                                           object_name.split('/')[-1]))
            if is_replace:
                with open(file_dir, 'wb') as file_data:
                    for d in data.stream(32 * 1024):
                        file_data.write(d)
                response = redirect('fileupload:documents_folder')
                response['Location'] += '?prefix={}'.format(file_path)
                root.destroy()
                return response

            else:
                response = redirect('fileupload:documents_folder')
                response['Location'] += '?prefix={}'.format(file_path)
                root.destroy()
                return response
        else:
            with open(file_dir, 'wb') as file_data:
                for d in data.stream(32 * 1024):
                    file_data.write(d)
            response = redirect('fileupload:documents_folder')
            response['Location'] += '?prefix={}'.format(file_path)
            root.destroy()
            return response

    except ResponseError as err:
        print(err)


def documents_download_v2(request):

    try:
        root = tkinter.Tk()
        root.withdraw()

        path = askdirectory(title='Select Folder')  # shows dialog box and return the path
        object_name = request.GET.get('object_name')
        file_dir = path + '/' + object_name.split('/')[-1]

        file_path = '/'.join(object_name.split('/')[:-1]) + '/'
        if file_path == '/':
            file_path = ''

        print(minioClient.fget_object(bucket_name, object_name, file_dir))
        root.destroy()

        response = redirect('fileupload:documents_folder')
        response['Location'] += '?prefix={}'.format(file_path)

        return response

    except ResponseError as err:
        print(err)

