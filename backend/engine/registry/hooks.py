class RegistryHooks:

    def __init__(self):
        self.before_register = []
        self.after_register = []

    def run_before(self, entity):
        for fn in self.before_register:
            fn(entity)

    def run_after(self, entity):
        for fn in self.after_register:
            fn(entity)