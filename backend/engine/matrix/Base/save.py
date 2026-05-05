def save(ctx):
    ctx.matrix.save_changes(ctx.request, ctx.changes)

    ctx.result = {
        "status": "ok",
        "effects": [
            {
                "type": "toast",
                "variant": "success",
                "message": "Сохранено",
            }
        ],
    }