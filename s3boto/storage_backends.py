from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_FILES_LOCATION #name of the media folder location
    file_overwrite = False