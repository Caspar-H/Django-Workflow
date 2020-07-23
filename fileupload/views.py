from django.http import HttpResponse
from django.shortcuts import render, redirect

from WorkflowEngine.settings import MINIO_HOST
from minio import Minio, ResponseError

import tkinter
import tkinter.messagebox as tkmb
from tkinter.filedialog import askdirectory, askopenfilename

import os

minioClient = Minio(MINIO_HOST,
                    access_key='tpg12345',
                    secret_key='tpg12345',
                    secure=False)
bucket_name = 'siteinfo'


# Create your views here.
def documents_folder(request):
    # documents_list(request)
    if request.method == 'GET':
        # Get object list
        objects = minioClient.list_objects(bucket_name, prefix=request.GET.get('prefix', ''), recursive=False)

        folder_list = []
        file_list = []
        current_path = prefix = request.GET.get('prefix', '')
        for obj in objects:
            # print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
            #       obj.etag, obj.size, obj.content_type, obj.is_dir)
            if obj.is_dir:
                folder_list.append({'folder_name': obj.object_name.split('/')[-2], 'object_name': obj.object_name,
                                    })
            else:
                if obj.size / 1024 < 1024:
                    file_size = str(round(obj.size / 1024, 2)) + 'KB'
                else:
                    file_size = str(round(obj.size / 1024 / 1024, 2)) + 'MB'
                file_list.append({'file_name': obj.object_name.split('/')[-1], 'last_modified': obj.last_modified,
                                  'object_name': obj.object_name, 'size': file_size})
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

        file_path = '/'.join(object_name.split('/')[:-1]) + '/'
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


def documents_upload(request):
    file_path = request.GET.get('prefix', '')

    try:
        root = tkinter.Tk()
        root.withdraw()
        file_location = askopenfilename()
        file_name = file_location.split('/')[-1]

        # If file is not selected, it will jump back to the folder.
        if not file_location:
            response = redirect('fileupload:documents_folder')
            response['Location'] += '?prefix={}'.format(file_path)
            root.destroy()
            return response

        # Check if file-name exists in the Minio Server
        objects_all = minioClient.list_objects(bucket_name, prefix=request.GET.get('prefix', ''), recursive=False)
        file_list = []
        current_path = prefix = request.GET.get('prefix', '')
        for obj in objects_all:
            if not obj.is_dir:
                file_list.append(obj.object_name.split('/')[-1])
        if file_name in file_list:
            is_replace = tkmb.askyesno("Replace or Skip Files",
                                       "The File Server already has a file named {} in this folder, do you want to "
                                       "replace it?".format(file_name))
            if is_replace:
                minio_object_name = file_path + file_name if file_path else file_name

                root.destroy()
                print(minioClient.fput_object(bucket_name, minio_object_name, file_location))

                response = redirect('fileupload:documents_folder')
                response['Location'] += '?prefix={}'.format(file_path)

                return response

            else:
                root.destroy()
                response = redirect('fileupload:documents_folder')
                response['Location'] += '?prefix={}'.format(file_path)
                return response
        else:

            minio_object_name = file_path + file_name if file_path else file_name

            root.destroy()
            print(minioClient.fput_object(bucket_name, minio_object_name, file_location))

            response = redirect('fileupload:documents_folder')
            response['Location'] += '?prefix={}'.format(file_path)

            return response

    except ResponseError as err:
        print(err)
        print("Unable to upload file. ")

        response = redirect('fileupload:documents_folder')
        response['Location'] += '?prefix={}'.format(file_path)

        return response


# def documents_list(request):
#     print('Documents List 1:')
#     objects_1 = minioClient.list_objects_v2(bucket_name, prefix='',
#                                           recursive=False, start_after='')
#     for obj in objects_1:
#         print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
#               obj.etag, obj.size, obj.content_type)
#
#     print('Documents List 2:')
#
#     objects_2 = minioClient.list_objects(bucket_name, prefix=request.GET.get('prefix', ''), recursive=True)
#     for obj in objects_2:
#         print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
#               obj.etag, obj.size, obj.content_type)
#
#     return None
def documents_folder_v2(request):
    return render(request, 'fileupload/documents_folder_v2.html', locals())
