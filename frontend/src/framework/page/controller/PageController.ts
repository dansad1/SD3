// src/framework/page/controller/PageController.ts

import { AuthContext } from "@/framework/auth/AuthContext"

import {
  useContext,
  useMemo,
} from "react"

import type { PageApi }
  from "../context/types"

import { buildPageRuntimeContext }
  from "../runtime/buildPageRuntimeContext"

import { usePageEventBus }
  from "../runtime/events/usePageEventBus"

import { usePageDebug }
  from "./hooks/usePageDebug"

import { usePageEffectsApi }
  from "./hooks/usePageEffectsApi"

import { usePageLoadingApi }
  from "./hooks/usePageLoadingApi"

import { usePageRouterRuntime }
  from "./hooks/usePageRouterRuntime"

import { usePageActionsRuntime }
  from "./usePageActionsRuntime"

import { usePageDataStore }
  from "./usePageDataStore"

import { usePageDirtyRuntime }
  from "./usePageDirtyRuntime"

import { usePageNavigation }
  from "./usePageNavigation"


export function usePageController() {
  const actionsRuntime =
    usePageActionsRuntime()

  const dirtyRuntime =
    usePageDirtyRuntime()

  const dataStore =
    usePageDataStore()

  const loading =
    usePageLoadingApi()

  const eventBus =
    usePageEventBus()

  const {
    params,
    query,
  } = usePageRouterRuntime()

  const {
    registerHandler,
    unregisterHandler,
    run,
    actions,
  } = actionsRuntime

  const auth =
    useContext(AuthContext)

  const user =
    auth?.me ?? null

  const runtimeContext = useMemo(() => {
    return buildPageRuntimeContext(
      params,
      query,
      {
        ...dataStore.data,
        ...dataStore.runtimeData,
      },
      actions,
      user,
    )
  }, [
    params,
    query,
    dataStore.data,
    dataStore.runtimeData,
    actions,
    user,
  ])

  const navigationContext = useMemo(() => {
    return buildPageRuntimeContext(
      params,
      query,
      {},
      [],
      user,
    )
  }, [
    params,
    query,
    user,
  ])

  const navigationRuntime =
    usePageNavigation(
      navigationContext
    )

  const {
    navigate,
  } = navigationRuntime

  const {
    setDirty,
    unregisterDirty,
    getPageDirty,
    pageDirty,
  } = dirtyRuntime

  const {
    setDataKey,
    getData,
    setRuntimeData,
  } = dataStore

  const effectsRuntime =
    usePageEffectsApi({
      navigate,
      setDataKey,
      emit: eventBus.emit,
    })

  const api: PageApi = useMemo(
    () => ({

      registerHandler,

      unregisterHandler,

      run,

      navigate,

      loading,

      setDirty,

      unregisterDirty,

      getPageDirty,

      setDataKey,

      getData,

      getRuntimeContext: () =>
        runtimeContext,

      setRuntimeData,

      runEffect:
        effectsRuntime.runEffect,

      runEffects:
        effectsRuntime.runEffects,

      emit:
        eventBus.emit,

      on:
        eventBus.on,

      query,

      params,

      getQuery: () =>
        query,

      getParams: () =>
        params,

    }),
    [
      registerHandler,
      unregisterHandler,
      run,
      navigate,
      loading,
      setDirty,
      unregisterDirty,
      getPageDirty,
      setDataKey,
      getData,
      runtimeContext,
      setRuntimeData,
      effectsRuntime.runEffect,
      effectsRuntime.runEffects,
      eventBus.emit,
      eventBus.on,
      query,
      params,
    ]
  )

  usePageDebug({
    runtimeContext,
    actions,
    registerHandler,
    unregisterHandler,
    run,
    pageDirty,
    setDirty,
    unregisterDirty,
    getPageDirty,
    data:
      dataStore.data,
    setDataKey,
    getData,
    start:
      loading.start,
    finish:
      loading.finish,
    isRunning:
      loading.isRunning,
    emit:
      eventBus.emit,
    on:
      eventBus.on,
    effectsRuntime,
    api,
  })

  return {
    api,
    actions,
    pageDirty,
    runtimeContext,
  }
}