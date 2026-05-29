import type { BlockComponent } from "../../Registry/BlockRegistry"
import { compileFormConfig } from "../config/compileFormConfig"
import type { FormApiBlock } from "../types/api"
import { FormBlock } from "./FormBlock"

export const FormDslBlock: BlockComponent<"form"> = ({ block, children }) => {

  const config = compileFormConfig(block as FormApiBlock)


  return (
    <FormBlock config={config}>
      {children}
    </FormBlock>
  )
}