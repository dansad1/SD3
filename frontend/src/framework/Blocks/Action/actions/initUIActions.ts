import { actionRegistry } from "../registry"



export function initUIActions() {

  actionRegistry.register({
    id: "ui.openFields",
    run: (ctx) => {

      ctx.modals?.visibleFields?.open?.()

      return true
    },
  })


  actionRegistry.register({
    id: "ui.openFilters",
    run: (ctx) => {

      console.log("🧹 ui.openFilters", ctx)

      ctx.modals?.filters?.open?.()

      return true
    },
  })


  actionRegistry.register({
    id: "ui.reloadTable",
    run: async (ctx) => {

      if (!ctx.list?.reload) {
        console.warn(
          "❌ ui.reloadTable: no reload handler"
        )

        return false
      }

      await ctx.list.reload()

      return true
    },
  })

}