import {
    useMemo,
    useState,
} from "react"

import Modal from "@/framework/components/ui/Modal"

import {
    useTableCollection,
} from "../controller/useTableCollection"

import type {
    BaseRow,
} from "../types/runtime"

type Id =
    | string
    | number

type Props = {

    isOpen: boolean

    onClose: () => void

    entity: string

    initial?: Id[]

    multiple?: boolean

    title?: string

    filter?: Record<
        string,
        unknown
    >

    onSubmit: (
        ids: Id[],
    ) => Promise<void>

    loading?: boolean

}

function getRowLabel(
    row: BaseRow,
): string {

    const data =
        row as Record<
            string,
            unknown
        >

    return String(

        data.label ??

        data.name ??

        data.username ??

        data.title ??

        row.id,

    )

}

export function EntityPickerModal({

    isOpen,

    onClose,

    entity,

    initial = [],

    multiple = true,

    title = "Выбор",

    filter,

    onSubmit,

    loading = false,

}: Props) {

    const [

        search,

        setSearch,

    ] = useState("")

    const [

        selected,

        setSelected,

    ] = useState<Set<Id>>(

        () => new Set(initial),

    )

    const collection =
        useTableCollection<BaseRow>(

            entity,

            {

                search,

                ...filter,

            },

            {

                enabled:
                    isOpen,

            },

        )

    const rows =
        collection.items

    const visibleRows =
        useMemo(

            () => rows,

            [rows],

        )

    function toggle(
        id: Id,
    ) {

        setSelected(
            prev => {

                const next =
                    new Set(prev)

                if (
                    multiple
                ) {

                    if (
                        next.has(id)
                    ) {

                        next.delete(id)

                    }

                    else {

                        next.add(id)

                    }

                }

                else {

                    next.clear()

                    next.add(id)

                }

                return next

            },
        )

    }

    async function save() {

        await onSubmit(

            Array.from(
                selected,
            ),

        )

    }

    return (

        <Modal

            isOpen={
                isOpen
            }

            onClose={
                onClose
            }

            width={900}

            title={
                title
            }

            footer={

                <>

                    <button

                        type="button"

                        className="ui-btn ui-btn-secondary"

                        disabled={
                            loading
                        }

                        onClick={
                            onClose
                        }

                    >

                        Отмена

                    </button>

                    <button

                        type="button"

                        className="ui-btn ui-btn-primary"

                        disabled={
                            loading
                        }

                        onClick={() => {

                            void save()

                        }}

                    >

                        {

                            loading

                                ? "..."

                                : "Сохранить"

                        }

                    </button>

                </>

            }

        >

            <input

                className="ui-input"

                placeholder="Поиск..."

                value={
                    search
                }

                onChange={

                    e =>

                        setSearch(
                            e.target.value,
                        )

                }

            />

            <div

                style={{

                    maxHeight:
                        500,

                    overflow:
                        "auto",

                    marginTop:
                        12,

                }}

            >

                {

                    visibleRows.map(

                        row => (

                            <label

                                key={
                                    String(
                                        row.id,
                                    )
                                }

                                style={{

                                    display:
                                        "flex",

                                    gap:
                                        8,

                                    padding:
                                        6,

                                    cursor:
                                        "pointer",

                                }}

                            >

                                <input

                                    type={

                                        multiple

                                            ? "checkbox"

                                            : "radio"

                                    }

                                    checked={

                                        selected.has(
                                            row.id,
                                        )

                                    }

                                    disabled={
                                        loading
                                    }

                                    onChange={() =>

                                        toggle(
                                            row.id,
                                        )

                                    }

                                />

                                <span>

                                    {

                                        getRowLabel(
                                            row,
                                        )

                                    }

                                </span>

                            </label>

                        ),

                    )

                }

            </div>

        </Modal>

    )

}