// ============================================================
// src/framework/Blocks/Matrix/MatrixBlock.tsx
// ============================================================

import {
  CapabilityBoundary,
} from "@/framework/security/CapabilityBoundary"

import {
  useCan,
} from "@/framework/security/useCan"

import {
  useMatrix,
} from "./runtime/useMatrix"

import {
  MatrixGrid,
} from "./MatrixGrid"

import {
  usePageRuntimeContext,
} from "@/framework/page/runtime/usePageRuntimeContext"

import {
  resolveObject,
} from "@/framework/bind/expression/resolveUnified"

import type {
  MatrixBlock as MatrixBlockType,
} from "./types"

type Props = {
  block: MatrixBlockType
}

export const MatrixBlock = ({
  block,
}: Props) => {

  const runtimeCtx =
    usePageRuntimeContext()

  /* =====================================================
     RESOLVE CONTEXT
     ===================================================== */

  const raw =
    block.params ??
    block.context

  const resolvedContext =
    raw
      ? resolveObject(
          raw,
          runtimeCtx
        )
      : raw

  console.log(
    "MATRIX RAW:",
    raw
  )

  console.log(
    "MATRIX RESOLVED:",
    resolvedContext
  )

  /* =====================================================
     MATRIX RUNTIME
     ===================================================== */

  const {
    data,
    updateCell,
  } = useMatrix(
    block.code,
    resolvedContext
  )

  /* =====================================================
     CAPABILITIES
     ===================================================== */

  const canEdit =
    useCan("edit", false)

  /* =====================================================
     LOADING
     ===================================================== */

  if (!data) {
    return <div>Loading...</div>
  }

  /* =====================================================
     RENDER
     ===================================================== */

  return (

    <CapabilityBoundary
      capabilities={
        data.capabilities
      }
    >

      <MatrixGrid

        layout={data.layout}

        cells={data.cells}

        onChange={
          canEdit
            ? updateCell
            : undefined
        }
      />

    </CapabilityBoundary>
  )
}