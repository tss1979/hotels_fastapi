import shutil
from fastapi import APIRouter, UploadFile

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router_images = APIRouter(prefix="/images", tags=["Картинки"])


@router_images.post("")
def upload_image(file: UploadFile):
    ImageService.upload_image(file)
