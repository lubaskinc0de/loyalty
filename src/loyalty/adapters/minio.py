import asyncio
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

    async def upload(self, file: BinaryIO, ext: str, size: int) -> str:
        fname = f"{uuid4()}.{ext}"
        await asyncio.to_thread(file.seek, 0)

        try:
            found_bucket = self.minio.bucket_exists(MINIO_BUCKET_NAME)
            if not found_bucket:
                logging.info("Created bucket %s", MINIO_BUCKET_NAME)
                await self.minio.make_bucket(MINIO_BUCKET_NAME)

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
