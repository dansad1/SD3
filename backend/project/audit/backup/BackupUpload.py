import shutil
import sqlite3
import uuid
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

from django.conf import settings

from backend.engine.action.Base.BaseAction import BaseAction


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"

DATABASE_FILENAME = "db.sqlite3"
MEDIA_ARCHIVE_FILENAME = "media.zip"
MEDIA_DIRECTORY_NAME = "media"

MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024
MAX_EXTRACTED_SIZE = 4 * 1024 * 1024 * 1024
MAX_ARCHIVE_FILES = 100_000


def error_response(message):
    return {
        "status": "error",
        "errors": {
            "__all__": [
                message,
            ],
        },
    }


def validate_uploaded_file(uploaded_file):
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValueError(
            "Размер загружаемого архива превышает допустимый лимит"
        )

    filename = str(uploaded_file.name or "").lower()

    if not filename.endswith(".zip"):
        raise ValueError(
            "Разрешены только ZIP-архивы"
        )


def normalize_member_name(filename):
    normalized = filename.replace("\\", "/")
    path = PurePosixPath(normalized)

    if path.is_absolute():
        raise ValueError(
            "ZIP содержит абсолютный путь"
        )

    if ".." in path.parts:
        raise ValueError(
            "ZIP содержит небезопасный путь"
        )

    clean_parts = [
        part
        for part in path.parts
        if part not in {
            "",
            ".",
        }
    ]

    if not clean_parts:
        return ""

    return "/".join(clean_parts)


def is_symbolic_link(member):
    unix_mode = member.external_attr >> 16

    return (
        unix_mode & 0o170000
    ) == 0o120000


def validate_member_path(
    member,
    target_dir,
):
    if is_symbolic_link(member):
        raise ValueError(
            "ZIP содержит символическую ссылку"
        )

    member_name = normalize_member_name(
        member.filename
    )

    if not member_name:
        return ""

    destination = (
        target_dir / member_name
    ).resolve()

    try:
        destination.relative_to(
            target_dir
        )
    except ValueError as exc:
        raise ValueError(
            "ZIP содержит небезопасный путь"
        ) from exc

    return member_name


def detect_archive_root(file_names):
    first_parts = {
        PurePosixPath(name).parts[0]
        for name in file_names
        if PurePosixPath(name).parts
    }

    if len(first_parts) != 1:
        return None

    candidate = next(iter(first_parts))

    database_path = (
        f"{candidate}/{DATABASE_FILENAME}"
    )

    if database_path in file_names:
        return candidate

    return None


def strip_archive_root(
    member_name,
    archive_root,
):
    if not archive_root:
        return member_name

    prefix = f"{archive_root}/"

    if member_name == archive_root:
        return ""

    if member_name.startswith(prefix):
        return member_name[len(prefix):]

    return member_name


def inspect_archive(
    archive,
    target_dir,
):
    members = archive.infolist()

    if len(members) > MAX_ARCHIVE_FILES:
        raise ValueError(
            "ZIP содержит слишком много файлов"
        )

    total_size = 0
    normalized_members = []

    for member in members:
        member_name = validate_member_path(
            member,
            target_dir,
        )

        if not member_name:
            continue

        if not member.is_dir():
            total_size += member.file_size

            if total_size > MAX_EXTRACTED_SIZE:
                raise ValueError(
                    "Распакованный архив превышает допустимый размер"
                )

        normalized_members.append(
            (
                member,
                member_name,
            )
        )

    file_names = {
        name
        for member, name in normalized_members
        if not member.is_dir()
    }

    archive_root = detect_archive_root(
        file_names
    )

    result = []

    for member, member_name in normalized_members:
        relative_name = strip_archive_root(
            member_name,
            archive_root,
        )

        if not relative_name:
            continue

        result.append(
            (
                member,
                relative_name,
            )
        )

    return result


def validate_archive_structure(members):
    file_names = {
        name
        for member, name in members
        if not member.is_dir()
    }

    if DATABASE_FILENAME not in file_names:
        raise ValueError(
            "В архиве отсутствует db.sqlite3"
        )

    has_media_archive = (
        MEDIA_ARCHIVE_FILENAME in file_names
    )

    has_media_directory = any(
        name.startswith(
            f"{MEDIA_DIRECTORY_NAME}/"
        )
        for name in file_names
    )

    if (
        has_media_archive
        and has_media_directory
    ):
        raise ValueError(
            "Архив должен содержать либо media.zip, "
            "либо папку media, но не оба варианта"
        )

    allowed_root_entries = {
        DATABASE_FILENAME,
        MEDIA_ARCHIVE_FILENAME,
        MEDIA_DIRECTORY_NAME,
    }

    for member, name in members:
        root_name = PurePosixPath(name).parts[0]

        if root_name not in allowed_root_entries:
            raise ValueError(
                f"Недопустимый объект в архиве: {name}"
            )

        if (
            root_name == DATABASE_FILENAME
            and name != DATABASE_FILENAME
        ):
            raise ValueError(
                "db.sqlite3 должен находиться в корне архива"
            )

        if (
            root_name == MEDIA_ARCHIVE_FILENAME
            and name != MEDIA_ARCHIVE_FILENAME
        ):
            raise ValueError(
                "media.zip должен находиться в корне архива"
            )


def extract_archive(
    archive,
    members,
    target_dir,
):
    for member, relative_name in members:
        destination = (
            target_dir / relative_name
        ).resolve()

        try:
            destination.relative_to(
                target_dir
            )
        except ValueError as exc:
            raise ValueError(
                "ZIP содержит небезопасный путь"
            ) from exc

        if member.is_dir():
            destination.mkdir(
                parents=True,
                exist_ok=True,
            )
            continue

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with archive.open(
            member,
            "r",
        ) as source:
            with destination.open(
                "wb",
            ) as target:
                shutil.copyfileobj(
                    source,
                    target,
                    length=1024 * 1024,
                )


def validate_sqlite_database(database_path):
    try:
        connection = sqlite3.connect(
            f"file:{database_path}?mode=ro",
            uri=True,
        )

        try:
            result = connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()
        finally:
            connection.close()

    except sqlite3.Error as exc:
        raise ValueError(
            "db.sqlite3 не является корректной SQLite-базой"
        ) from exc

    if not result or result[0] != "ok":
        raise ValueError(
            "Проверка целостности db.sqlite3 завершилась ошибкой"
        )


def validate_media_archive(media_archive_path):
    try:
        with zipfile.ZipFile(
            media_archive_path,
            "r",
        ) as archive:
            bad_file = archive.testzip()
    except zipfile.BadZipFile as exc:
        raise ValueError(
            "media.zip повреждён или имеет неверный формат"
        ) from exc

    if bad_file:
        raise ValueError(
            f"Повреждён файл внутри media.zip: {bad_file}"
        )


def create_media_archive(
    extracted_folder,
):
    media_directory = (
        extracted_folder / MEDIA_DIRECTORY_NAME
    )

    media_archive = (
        extracted_folder / MEDIA_ARCHIVE_FILENAME
    )

    if media_archive.exists():
        validate_media_archive(
            media_archive
        )
        return

    if media_directory.exists():
        if not media_directory.is_dir():
            raise ValueError(
                "media должен быть каталогом"
            )

        archive_base = (
            extracted_folder / "media"
        )

        shutil.make_archive(
            base_name=str(archive_base),
            format="zip",
            root_dir=str(media_directory),
        )

        shutil.rmtree(
            media_directory,
            ignore_errors=True,
        )

        return

    with zipfile.ZipFile(
        media_archive,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ):
        pass


class BackupUploadAction(BaseAction):
    code = "backup.upload"
    permission = "upload_backups"

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        uploaded_file = request.FILES.get(
            "file"
        )

        if not uploaded_file:
            return error_response(
                "Файл не выбран"
            )

        try:
            validate_uploaded_file(
                uploaded_file
            )
        except ValueError as exc:
            return error_response(
                str(exc)
            )

        folder_name = (
            datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
            + "_"
            + uuid.uuid4().hex[:6]
        )

        BACKUP_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_folder = (
            BACKUP_DIR
            / f".{folder_name}.uploading"
        )

        backup_folder = (
            BACKUP_DIR / folder_name
        )

        uploaded_zip_path = (
            temporary_folder / "uploaded.zip"
        )

        try:
            temporary_folder.mkdir(
                parents=True,
                exist_ok=False,
            )

            with uploaded_zip_path.open(
                "wb"
            ) as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(
                        chunk
                    )

            with zipfile.ZipFile(
                uploaded_zip_path,
                "r",
            ) as archive:
                members = inspect_archive(
                    archive,
                    temporary_folder,
                )

                validate_archive_structure(
                    members
                )

                extract_archive(
                    archive,
                    members,
                    temporary_folder,
                )

            uploaded_zip_path.unlink(
                missing_ok=True
            )

            database_path = (
                temporary_folder
                / DATABASE_FILENAME
            )

            validate_sqlite_database(
                database_path
            )

            create_media_archive(
                temporary_folder
            )

            if backup_folder.exists():
                raise ValueError(
                    "Бэкап с таким именем уже существует"
                )

            temporary_folder.rename(
                backup_folder
            )

            return {
                "status": "ok",
                "message": (
                    f"Бэкап {folder_name} "
                    "успешно загружен"
                ),
                "effects": [
                    {
                        "type": "table.reload",
                        "entity": "backup",
                    },
                    {
                        "type": "toast",
                        "variant": "success",
                        "message": (
                            "Резервная копия загружена"
                        ),
                    },
                ],
            }

        except zipfile.BadZipFile:
            shutil.rmtree(
                temporary_folder,
                ignore_errors=True,
            )

            return error_response(
                "Файл не является корректным ZIP-архивом"
            )

        except ValueError as exc:
            shutil.rmtree(
                temporary_folder,
                ignore_errors=True,
            )

            return error_response(
                str(exc)
            )

        except OSError:
            shutil.rmtree(
                temporary_folder,
                ignore_errors=True,
            )

            return error_response(
                "Не удалось сохранить резервную копию"
            )