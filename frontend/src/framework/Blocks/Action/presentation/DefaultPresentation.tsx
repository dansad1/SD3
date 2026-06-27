import {
    useActionExecutor
}
from "../executor/useActionExecutor"

import type {
    ActionBlock
}
from "../types"



export function DefaultPresentation(

props:ActionBlock

){

const {

runAction,

isRunning,

}

=

useActionExecutor()



const finalAction=

props.action ??

props.to


if(

!finalAction

){

return null

}


const loading=

isRunning(

finalAction

)



return(

<button


type="button"


className={[

"ui-btn",

`ui-btn-${props.variant}`,

"ui-btn-md",

loading &&

"is-loading",

]

.filter(Boolean)

.join(" ")}


disabled={

loading

}


aria-busy={

loading

}


onClick={()=>{

void runAction(

finalAction,

props.ctx

)

}}

>


<span

className=

"ui-btn-label"

>

{

loading

?

"..."

:

props.label

}

</span>

</button>

)

}