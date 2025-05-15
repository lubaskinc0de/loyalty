import logging
from dataclasses import dataclass
from typing import BinaryIO
from uuid import uuid4

from minio import Minio
from minio.error import MinioException

from loyalty.adapters.config_loader import StorageConfig
from loyalty.application.common.file_manager import FileManager
from loyalty.application.exceptions.base import ApplicationError

MINIO_BUCKET_NAME = "images"


class FileUploadError(ApplicationError): ...


@dataclass(slots=True, frozen=True)
class MinioFileManager(FileManager):
    minio: Minio
    config: StorageConfig

    def _make_bucket(self) -> None:
        found_bucket = self.minio.bucket_exists(MINIO_BUCKET_NAME)
        if not found_bucket:
            logging.info("Created bucket %s", MINIO_BUCKET_NAME)
            self.minio.make_bucket(MINIO_BUCKET_NAME)

    def upload(self, file: BinaryIO, ext: str, size: int) -> str:
        fname = f"{uuid4()}.{ext}"
        file.seek(0)

        try:
            self._make_bucket()
            info = self.minio.put_object(
                MINIO_BUCKET_NAME,
                fname,
                file,
                length=size,
                part_size=5 * 1024 * 1024,
            )
            file_path = f"{self.config.file_server}/{info.object_name}"
        except MinioException as exc:
            logging.exception("While uploading image to Minio")
            raise FileUploadError from exc

        return file_path

    def remove(self, file_url: str) -> None:
        fname = file_url.split("/")[-1]
        try:
            self._make_bucket()
            self.minio.remove_object(MINIO_BUCKET_NAME, fname)
        except MinioException as exc:
            logging.exception("While deleting image from Minio")
            raise FileUploadError from exc
