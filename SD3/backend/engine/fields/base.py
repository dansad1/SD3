class BaseField:
    """
    Абстрактное описание поля (НЕ значение)
    """

    def __init__(self, source):
        self.source = source

    @property
    def name(self):
        raise NotImplementedError

    @property
    def label(self):
        return getattr(self.source, "label", self.name)

    @property
    def required(self):
        return getattr(self.source, "required", False)

    @property
    def type(self):
        raise NotImplementedError

    @property
    def choices(self):
        return []