from fastapi import BackgroundTasks, Depends
from .service import MailService


def get_mail_service(bg_task: BackgroundTasks) -> MailService:
    return MailService(bg_task)
