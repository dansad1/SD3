from django.shortcuts import get_object_or_404

def load_instance(ctx):
    if not ctx.pk:
        ctx.instance = None
        return

    qs = ctx.entity.get_queryset(ctx.request)
    ctx.instance = get_object_or_404(qs, pk=ctx.pk)