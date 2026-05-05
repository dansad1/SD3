def all_subclasses(cls):
    result = set()

    for subclass in cls.__subclasses__():
        result.add(subclass)
        result.update(all_subclasses(subclass))

    return result