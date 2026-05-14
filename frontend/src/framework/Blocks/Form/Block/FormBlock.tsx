// src/framework/Blocks/Form/Block/FormBlock.tsx

import {
  useEffect,
  useMemo,
  type ReactNode,
} from "react"

import { FormRenderer }
  from "../render/FormRenderer"

import {
  useFormController,
} from "../controller/useFormController"

import {
  usePageApi,
} from "@/framework/page/context/usePageApi"

import type {
  FormConfig,
} from "../types/FormConfig"

import {
  getFormScope,
} from "../controller/getFormScope"

import {
  applyLayoutConfig,
} from "../config/FormLayoutCompiler"

import type {
  FormSchema,
} from "../types/types"

import {
  FormContext,
} from "../context/FormContext"

import {
  useActionsByPlacement,
} from "../../Action/handlers/useActionsByPlacement"

type Props = {
  config: FormConfig
  children?: ReactNode
}

export function FormBlock({
  config,
  children,
}: Props) {

  // =====================================================
  // VALIDATE
  // =====================================================

  if (!config) {

    throw new Error(
      "FormBlock used without config"
    )
  }

  // =====================================================
  // SCOPE
  // =====================================================

  const { scope } = useMemo(
    () => getFormScope(config),
    [config]
  )

  // =====================================================
  // FORM
  // =====================================================

  const form =
    useFormController(config)

  // =====================================================
  // PAGE API
  // =====================================================

  const { setRuntimeData } =
    usePageApi()

  // =====================================================
  // ENTITY
  // =====================================================

  const entity =
    config.formType === "entity"
      ? config.entity
      : null

  // =====================================================
  // SCHEMA
  // =====================================================

  const schema:
    FormSchema | null =
      form.schema

  const finalSchema =
    useMemo(() => {

      if (!schema) {
        return null
      }

      return applyLayoutConfig(
        schema,
        config.formLayout,
      )

    }, [
      schema,
      config.formLayout,
    ])

  // =====================================================
  // FORM ACTIONS
  // =====================================================

  const formActions =
    useActionsByPlacement(
      "form"
    )

  // =====================================================
  // SYNC DATA
  // =====================================================

  useEffect(() => {

    if (!entity) return

    if (!form.values) return

    setRuntimeData(entity, {
      ...form.values,
    })

  }, [
    entity,
    form.values,
    setRuntimeData,
  ])

  // =====================================================
  // LOADING
  // =====================================================

  if (
    form.loading ||
    !finalSchema
  ) {
    return null
  }

  // =====================================================
  // DEBUG
  // =====================================================

  console.log(
    "🧪 FORM ERRORS",
    form.fieldErrors
  )

  // =====================================================
  // RENDER
  // =====================================================

  return (

    <FormContext.Provider
      value={form}
    >

      <>

        <FormRenderer

          key={scope}

          schema={finalSchema}

          values={form.values}

          fieldErrors={
            form.fieldErrors
          }

          formError={
            form.formError
          }

          onChange={
            form.setValue
          }

          actions={
            formActions
          }
        />

        {children}

      </>

    </FormContext.Provider>
  )
}