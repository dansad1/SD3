import JournalPrint from "@/Project/custom/JournalPrint"

const registry: Record<string, any> = {
  JournalPrint,
}

export const CustomBlock = ({ block }: any) => {
  const Component = registry[block.component]

  if (!Component) {
    return <div>Unknown component: {block.component}</div>
  }

  return <Component {...(block.props || {})} />
}