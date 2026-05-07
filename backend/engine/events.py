LISTENERS = {}


def listen(
    event,
    listener,
):

    LISTENERS.setdefault(
        event,
        [],
    ).append(listener)


def emit(
    event,
    **payload,
):

    listeners = LISTENERS.get(
        event,
        []
    )

    for listener in listeners:
        listener(**payload)