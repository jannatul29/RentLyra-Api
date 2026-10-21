from abc import ABC

from django.core.files.storage import FileSystemStorage


class ProfileImageMediaStorage(FileSystemStorage, ABC):
    location = 'data/media/photos/profile-image'
