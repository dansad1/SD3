# backend/project/tickets/utils/upload_paths.py

import uuid
from pathlib import Path


def ticket_attachment_upload_path(
    instance,
    filename,
):

    ext = Path(filename).suffix

    generated = uuid.uuid4().hex

    return (
        f"tickets/"
        f"{instance.ticket_id or 'temp'}/"
        f"{generated}{ext}"
    )