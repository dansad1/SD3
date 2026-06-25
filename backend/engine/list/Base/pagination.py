from django.core.paginator import EmptyPage
from django.core.paginator import Paginator


DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 300


def get_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def paginate(ctx):
    page_size = get_int(
        ctx.request.GET.get("page_size"),
        DEFAULT_PAGE_SIZE,
    )

    page_size = max(
        1,
        min(page_size, MAX_PAGE_SIZE),
    )

    page_number = get_int(
        ctx.request.GET.get("page"),
        1,
    )

    paginator = Paginator(
        ctx.qs,
        page_size,
    )

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    ctx.paginator = paginator
    ctx.page = page
    ctx.qs = page.object_list