from django.core.paginator import Paginator


def paginate(ctx):
    try:
        size = int(ctx.request.GET.get("page_size", 500))
    except Exception:
        size = 500

    size = max(1, min(size, 300))

    paginator = Paginator(ctx.qs, size)
    page = paginator.get_page(ctx.request.GET.get("page", 1))

    ctx.paginator = paginator
    ctx.page = page