import { FieldRenderer }
from "@/framework/Blocks/Form/render/FieldRenderer"

import Button
from "../../ui/Button"

import Modal
from "../../ui/Modal"

import { useFilterRuntime }
from "./useFilterRuntime"


interface Props {

    isOpen:boolean

    onClose:()=>void

    entity:string

    fieldset?:string

    initialQuery?:Record<
        string,
        string
    >

    onApply?:(
        q:Record<
            string,
            string
        >
    )=>void

}



export default function FilterModal({

    isOpen,

    onClose,

    entity,

    fieldset="default",

    initialQuery={},

    onApply,

}:Props){

const {

    loading,

    fields,

    values,

    setValues,

    buildEmptyValues,

    buildQuery,

}=useFilterRuntime(

    entity,

    fieldset,

    initialQuery,

)


if(!isOpen){

    return null

}



return(

<Modal

title="Фильтр"

isOpen={isOpen}

onClose={onClose}

width={900}


footer={

<>

<Button

variant="secondary"

onClick={()=>{

setValues(

buildEmptyValues(

fields

)

)

}}

>

Сбросить

</Button>



<Button

onClick={()=>{

onApply?.(

buildQuery()

)

onClose()

}}

>

Применить

</Button>


</>

}


>


{

loading

&&

<div>

Загрузка...

</div>

}



{

!loading

&&

<div

style={{

display:"grid",

gridTemplateColumns:

"1fr 1fr",

gap:16,

}}

>

{

fields.map(

field=>(

<FieldRenderer

key={

field.name

}

field={

field

}

value={

values[

field.name

]

}

errors={[]}


onChange={

value=>{

setValues(

prev=>({

...prev,

[field.name]:

value

})

)

}

}


setFieldValue={()=>{}}


/>

)

)

}


</div>

}


</Modal>

)

}