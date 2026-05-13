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

  // =====================================================
  // RUNTIMES
  // =====================================================

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

  // =====================================================
  // ACTIONS
  // =====================================================

  const {
    registerHandler,
    unregisterHandler,
    run,
    actions,
  } = actionsRuntime

  // =====================================================
  // AUTH
  // =====================================================

  const auth =
    useContext(AuthContext)

  const user =
    auth?.me ?? null

  // =====================================================
  // RUNTIME CONTEXT
  // =====================================================

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

  /*
    navigationRuntime НЕ должен зависеть
    от page data иначе можно поймать
    infinite loop при form sync
  */

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

  // =====================================================
  // NAVIGATION
  // =====================================================

  const navigationRuntime =
    usePageNavigation(
      navigationContext
    )

  const {
    navigate,
  } = navigationRuntime

  // =====================================================
  // DIRTY
  // =====================================================

  const {
    setDirty,
    unregisterDirty,
    getPageDirty,
    pageDirty,
  } = dirtyRuntime

  // =====================================================
  // DATA
  // =====================================================

  const {
    setDataKey,
    getData,
    setRuntimeData,
  } = dataStore

  // =====================================================
  // EFFECTS
  // =====================================================

  const effectsRuntime =
    usePageEffectsApi({

      navigate,

      setDataKey,

      emit: eventBus.emit,
    })

  // =====================================================
  // API
  // =====================================================

  const api: PageApi = useMemo(
    () => ({

      // ===============================================
      // ACTIONS
      // ===============================================

      registerHandler,

      unregisterHandler,

      run,

      navigate,

      // ===============================================
      // LOADING
      // ===============================================

      loading,

      // ===============================================
      // DIRTY
      // ===============================================

      setDirty,

      unregisterDirty,

      getPageDirty,

      // ===============================================
      // DATA
      // ===============================================

      setDataKey,

      getData,

      setRuntimeData,

      // ===============================================
      // EFFECTS
      // ===============================================

      runEffect:
        effectsRuntime.runEffect,

      runEffects:
        effectsRuntime.runEffects,

      // ===============================================
      // EVENTS
      // ===============================================

      emit:
        eventBus.emit,

      on:
        eventBus.on,

      // ===============================================
      // ROUTER
      // ===============================================

      query,

      params,

      getQuery: () => query,

      getParams: () => params,

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

      setRuntimeData,

      effectsRuntime.runEffect,

      effectsRuntime.runEffects,

      eventBus.emit,

      eventBus.on,

      query,

      params,
    ]
  )

  // =====================================================
  // DEBUG
  // =====================================================

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

  // =====================================================
  // RETURN
  // =====================================================

  return {

    api,

    actions,

    pageDirty,

    runtimeContext,
  }
}