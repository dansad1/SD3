import type { BlockComponent } from "../../Registry/BlockRegistry"
import { compileFormConfig } from "../config/compileFormConfig"
import type { FormApiBlock } from "../types/api"
import { FormBlock } from "./FormBlock"

export const FormDslBlock: BlockComponent<"form"> = ({ block, children }) => {
  console.log("🔥 DSL BLOCK:", block)

  const config = compileFormConfig(block as FormApiBlock)

  console.log("🔥 COMPILED CONFIG:", config)

  return (
    <FormBlock config={config}>
      {children}
    </FormBlock>
  )
}