from SD3.backend.engine.form.BaseForm import BaseForm


class AutoEntityForm(BaseForm):

    def __init__(self, entity):
        self.entity = entity
        self.code = f"{entity.entity}.form"