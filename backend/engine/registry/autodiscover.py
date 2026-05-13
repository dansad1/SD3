def all_subclasses(cls):

    result = []

    for sub in cls.__subclasses__():

        result.append(sub)

        result.extend(
            all_subclasses(sub)
        )

    return result