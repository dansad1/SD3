import { actionRegistry } from "../registry"



export function initUIActions() {
  actionRegistry.register({
    id: "ui.openFields",
    run: (ctx) => {
      console.log("🖥 ui.openFields", ctx)

      ctx.modals?.visibleFields?.open?.()

      return true
    },
  })

 actionRegistry.register({
  id: "ui.reloadTable",
  run: async (ctx) => {
    console.log("🔄 ui.reloadTable ctx", ctx)
    console.log("🔄 ui.reloadTable list", ctx.list)
    console.log("🔄 ui.reloadTable reload", ctx.list?.reload)

    if (!ctx.list?.reload) {
      console.warn("❌ ui.reloadTable: no reload handler")
      return false
    }

    try {
      await ctx.list.reload()

      console.log("✅ ui.reloadTable reload complete")

      return true
    } catch (e) {
      console.error("❌ ui.reloadTable reload error", e)
      return false
    }
  },
})

  console.log(
    "🖥 UI ACTIONS REGISTERED",
    actionRegistry.all().map(x => x.id)
  )
}