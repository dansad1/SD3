from django.db import models

from backend.generic.models.BaseFieldSet import BaseFieldSet
from backend.project.companies.models import CompanyFieldSet
from backend.project.tickets.models import TicketFieldSet


class UserFieldSet(BaseFieldSet):
    def __str__(self):
        return self.name



