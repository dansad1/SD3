import { useState } from "react"

import { EntityPickerModal } from "../../Table/features/RelationPickerModal"

import { useActionExecutor } from "../executor/useActionExecutor"

import type {
    ActionBlock,
} from "../types"

export function PickerPresentation(
    props: ActionBlock,
) {
    const [open, setOpen] =
        useState(false)

    const {
        runAction,
        isRunning,
    } = useActionExecutor()

    if (!props.picker) {
        return null
    }

    const picker = props.picker

    function getActionId(): string {
        const id =
            props.action ??
            props.to

        if (!id) {
            throw new Error(
                "ActionBlock: action or to is required.",
            )
        }

        return id
    }

    const actionId =
        getActionId()

    const loading =
        isRunning(actionId)

    async function handleSubmit(
        ids: (
            string |
            number
        )[],
    ) {
        const ok =
            await runAction(
                actionId,
                {
                    ...props.ctx,

                    extra: {
                        ...props.ctx?.extra,

                        ids,
                    },
                },
            )

        if (ok !== false) {
            setOpen(false)
        }
    }

    function handleOpen() {
        if (loading) {
            return
        }

        setOpen(true)
    }

    function handleClose() {
        if (loading) {
            return
        }

        setOpen(false)
    }

    return (
        <>
            <button
                type="button"
                className={[
                    "ui-btn",

                    `ui-btn-${props.variant ?? "secondary"}`,

                    "ui-btn-md",

                    loading &&
                        "is-loading",
                ]
                    .filter(Boolean)
                    .join(" ")}
                disabled={loading}
                aria-busy={loading}
                onClick={handleOpen}
            >
                <span className="ui-btn-label">
                    {loading
                        ? "..."
                        : props.label}
                </span>
            </button>

            {open && (
                <EntityPickerModal
                    isOpen={open}
                    onClose={handleClose}
                    entity={picker.entity}
                    title={picker.title}
                    multiple={picker.multiple}
                    filter={picker.filter}
                    onSubmit={handleSubmit}
                />
            )}
        </>
    )
}