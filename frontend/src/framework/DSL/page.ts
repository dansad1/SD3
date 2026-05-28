// src/framework/DSL/page.ts

import type {
  DSLNode,
} from "./runtime"

import {
  compileDSL,
} from "./compile"

import type {
  ApiPageSchema,
  PageChrome,
} from "../page/PageSchema"

/* ===================================================== */
/* OPTIONS */
/* ===================================================== */

export interface PageOptions {

  title?: string

  chrome?: PageChrome

  /*
    🔐 AUTH REQUIRED

    default:
    true
  */

  auth?: boolean

  /*
    👤 ONLY FOR ANONYMOUS USERS

    login/register/reset-password
  */

  guestOnly?: boolean
}

/* ===================================================== */
/* PAGE */
/* ===================================================== */

export function page(

  id: string,

  optionsOrRoot:
    | DSLNode
    | PageOptions,

  maybeRoot?: DSLNode,

): ApiPageSchema {

  /* ==================================== */
  /* RESOLVE SIGNATURE */
  /* ==================================== */

  let options:
    PageOptions = {}

  let root: DSLNode

  /*
    page(id, root)
  */

  if (
    maybeRoot === undefined
  ) {

    root =
      optionsOrRoot as DSLNode
  }

  /*
    page(id, options, root)
  */

  else {

    options =
      optionsOrRoot as PageOptions

    root = maybeRoot
  }

  /* ==================================== */
  /* COMPILE */
  /* ==================================== */

  const blocks =
    compileDSL(root)

  /* ==================================== */
  /* SCHEMA */
  /* ==================================== */

  return {

    id,

    title:
      options.title,

    chrome:
      options.chrome,

    /*
      🔐 AUTH
    */

    auth:
      options.auth,

    /*
      👤 GUEST ONLY
    */

    guestOnly:
      options.guestOnly,

    /*
      📦 BLOCKS
    */

    blocks,
  }
}