import NotificationOverview from "@/Project/notifications/NotificationOverview/overview"

const registry: Record<string, any> = {
    NotificationOverview,
}

export const CustomBlock = ({ block }: any) => {
  const Component = registry[block.component]

  if (!Component) {
    return <div>Unknown component: {block.component}</div>
  }

  return <Component {...(block.props || {})} />
}