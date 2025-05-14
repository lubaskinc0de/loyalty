from typing import BinaryIO

import filetype  # type: ignore


def is_valid_image(file_stream: BinaryIO) -> bool:
    """Проверяет, является ли файл валидным изображением, используя filetype."""
    position = file_stream.tell()
    file_stream.seek(0)
    kind = filetype.guess(file_stream)
    file_stream.seek(position)
    return kind is not None and kind.mime.startswith("image/")
