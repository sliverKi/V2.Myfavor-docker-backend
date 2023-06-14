from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    bucket_name = 'myfavor-s3-bucket'
    location = 'media'
    file_overwrite = False