import cloudinary.uploader
from django.conf import settings
from django.core.files.storage import default_storage
from pathlib import Path


def upload_avatar(file, user_id: str) -> str:
    try:
        result = cloudinary.uploader.upload(
            file,
            folder='apex/avatars',
            public_id=f'user_{user_id}',
            overwrite=True,
            resource_type='image',
            transformation=[{'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'}],
        )
        return result['secure_url']
    except Exception:
        extension = Path(file.name).suffix.lower() or '.jpg'
        filename = f'avatars/user_{user_id}{extension}'
        if default_storage.exists(filename):
            default_storage.delete(filename)
        saved_name = default_storage.save(filename, file)
        return f'{settings.MEDIA_URL}{saved_name}'


def upload_evidence(file, job_id: str, index: int) -> str:
    result = cloudinary.uploader.upload(
        file,
        folder='apex/evidence',
        public_id=f'job_{job_id}_ev_{index}',
        overwrite=True,
        resource_type='auto',
    )
    return result['secure_url']
