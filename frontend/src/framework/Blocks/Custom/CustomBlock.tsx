
const registry: Record<string, any> = {
}

export const CustomBlock = ({ block }: any) => {
  const Component = registry[block.component]

  if (!Component) {
    return <div>Unknown component: {block.component}</div>
  }

  return <Component {...(block.props || {})} />
}