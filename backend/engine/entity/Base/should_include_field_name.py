# -------------------------
# FIELD NAME FILTER (для dict / ресурсов)
# -------------------------

def should_include_field_name(self, name: str):

    # системный мусор
    if name in self.system_exclude_fields:
        return False

    # exclude
    if self.exclude_fields and name in self.exclude_fields:
        return False

    # include
    if self.include_fields is not None:
        return name in self.include_fields

    return True


def should_include_in_list(self, name: str):
    return self.should_include_field_name(name)