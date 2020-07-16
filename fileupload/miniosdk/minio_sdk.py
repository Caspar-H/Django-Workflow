from minio import Minio

minio_host_name = '127.0.0.1:9000'

minioClient = Minio(minio_host_name,
                    access_key='tpg12345',
                    secret_key='tpg12345',
                    secure=False)


def list_objects(bucket_name, prefix=None, recursive=False):
    # List all object paths in bucket that begin with my-prefixname.
    objects = minioClient.list_objects(bucket_name, prefix=prefix,
                                       recursive=recursive)
    for obj in objects:
        print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
              obj.etag, obj.size, obj.content_type)

