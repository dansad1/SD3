import { useEffect } from "react"

type Params = {
  runtimeContext: unknown
  actions: unknown[]
  registerHandler: unknown
  unregisterHandler: unknown
  run: unknown
  pageDirty: boolean
  setDirty: unknown
  unregisterDirty: unknown
  getPageDirty: unknown
  data: unknown
  setDataKey: unknown
  getData: unknown
  start: unknown
  finish: unknown
  isRunning: unknown
  emit: unknown
  on: unknown
  effectsRuntime: {
    runEffect: unknown
    runEffects: unknown
  }
  api: unknown
}

export function usePageDebug({
  runtimeContext,
  actions,
  registerHandler,
  unregisterHandler,
  run,
  pageDirty,
  setDirty,
  unregisterDirty,
  getPageDirty,
  data,
  setDataKey,
  getData,
  start,
  finish,
  isRunning,
  emit,
  on,
  effectsRuntime,
  api,
}: Params) {
  useEffect(() => {
    console.log("[PageController] mounted")
  }, [])

  useEffect(() => {
    console.log("[PageController] runtimeContext", runtimeContext)
  }, [runtimeContext])

  useEffect(() => {
    console.log("[PageController] actionsRuntime", {
      actions,
      hasRegisterHandler: !!registerHandler,
      hasUnregisterHandler: !!unregisterHandler,
      hasRun: !!run,
    })
  }, [actions, registerHandler, unregisterHandler, run])

  useEffect(() => {
    console.log("[PageController] dirtyRuntime", {
      pageDirty,
      hasSetDirty: !!setDirty,
      hasUnregisterDirty: !!unregisterDirty,
      hasGetPageDirty: !!getPageDirty,
    })
  }, [
    pageDirty,
    setDirty,
    unregisterDirty,
    getPageDirty,
  ])

  useEffect(() => {
    console.log("[PageController] dataStore", {
      data,
      hasSetDataKey: !!setDataKey,
      hasGetData: !!getData,
    })
  }, [data, setDataKey, getData])

  useEffect(() => {
    console.log("[PageController] loadingRuntime", {
      hasStart: !!start,
      hasFinish: !!finish,
      hasIsRunning: !!isRunning,
    })
  }, [start, finish, isRunning])

  useEffect(() => {
    console.log("[PageController] eventBus", {
      hasEmit: !!emit,
      hasOn: !!on,
    })
  }, [emit, on])

  useEffect(() => {
    console.log("[PageController] effectsRuntime", effectsRuntime)
  }, [effectsRuntime])

  useEffect(() => {
    console.log("[PageController] api ready", api)
  }, [api])
}