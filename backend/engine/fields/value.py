class BaseValueAccessor:

    def get(self, obj, field):
        raise NotImplementedError

    def set(self, obj, field, value):
        raise NotImplementedError