import email
import imaplib

from email.header import decode_header
from email.utils import parseaddr


class IMAPEmailReceiver:

    def __init__(self, settings):
        self.settings = settings

    def fetch_unseen(self):
        imap = self.get_connection()

        try:
            imap.login(
                self.settings.username,
                self.settings.password,
            )
            imap.select("INBOX")

            status, numbers = imap.search(None, "UNSEEN")

            if status != "OK":
                return []

            messages = []

            for number in numbers[0].split():
                status, data = imap.fetch(number, "(RFC822)")

                if status != "OK":
                    continue

                raw_message = data[0][1]
                message = email.message_from_bytes(raw_message)

                messages.append(
                    self.parse_message(message)
                )

            return messages

        finally:
            try:
                imap.logout()
            except Exception:
                pass

    def get_connection(self):
        if self.settings.use_ssl:
            return imaplib.IMAP4_SSL(
                self.settings.host,
                self.settings.port,
            )

        return imaplib.IMAP4(
            self.settings.host,
            self.settings.port,
        )

    def parse_message(self, message):
        return {
            "from_email": self.get_from_email(message),
            "subject": self.get_subject(message),
            "body": self.get_body(message),
            "attachments": self.get_attachments(message),
        }

    def get_from_email(self, message):
        return parseaddr(
            message.get("From", "")
        )[1]

    def get_subject(self, message):
        subject = message.get("Subject", "")

        decoded = decode_header(subject)
        parts = []

        for value, encoding in decoded:
            if isinstance(value, bytes):
                parts.append(
                    value.decode(
                        encoding or "utf-8",
                        errors="ignore",
                    )
                )
            else:
                parts.append(value)

        return "".join(parts).strip()

    def get_body(self, message):
        body = ""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_disposition() == "attachment":
                    continue

                if part.get_content_type() != "text/plain":
                    continue

                payload = part.get_payload(decode=True)

                if payload:
                    body += payload.decode(
                        part.get_content_charset() or "utf-8",
                        errors="ignore",
                    )

            return body.strip()

        payload = message.get_payload(decode=True)

        if not payload:
            return ""

        return payload.decode(
            message.get_content_charset() or "utf-8",
            errors="ignore",
        ).strip()

    def get_attachments(self, message):
        attachments = []

        if not message.is_multipart():
            return attachments

        for part in message.walk():
            if part.get_content_disposition() != "attachment":
                continue

            filename = part.get_filename()
            content = part.get_payload(decode=True)

            if filename and content:
                attachments.append({
                    "name": filename,
                    "content": content,
                })

        return attachments