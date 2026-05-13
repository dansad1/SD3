// src/framework/DSL/language.ts
/* =========================================================
   UI COMPOSITION LANGUAGE (DSL)
   Page-driven, Entity-driven
   Framework V1
   ========================================================= */

/**
 * ВАЖНО:
 * 1) Это описание ЯЗЫКА (контракта props), а не бизнес-логики.
 * 2) DSL-типизация глубже делается в compile/runtime, здесь — allowed-shape.
 */

export type Primitive =
  | "string"
  | "number"
  | "boolean"
  | "array"
  | "object"
  | "any"
/* =========================
   LAYOUT (PHYSICAL GRID)
   ========================= */

export const Layout = {
  span: [1, 2, 3, 4, 6, 12] as const,
  area: ["main", "sidebar-left", "sidebar-right", "overlay"] as const,
} as const

/* =========================
   BASE BLOCK
   ========================= */

export const Block = {
  props: {
    layout: {
      span: Layout.span,
      order: "number" as Primitive,
      hidden: "boolean" as Primitive,
      area: Layout.area,
    },
  },
} as const

/* =========================
   STRUCTURAL (COMPOSITION)
   ========================= */

export const Structural = {

  container: {
    props: {
      maxWidth: ["xs", "sm", "md", "lg", "xl"] as const,
      align: ["left", "center", "right"] as const,
      padding: ["none", "sm", "md", "lg"] as const,
    },
  },

  stack: {
    props: {
      gap: ["none", "sm", "md", "lg"] as const,
      align: ["start", "center", "end", "stretch"] as const,
      variant: ["default", "card"] as const,
    },
  },

  split: {
    props: {
      ratio: "string" as Primitive,
      gap: ["none", "sm", "md", "lg"] as const,
      responsive: "boolean" as Primitive,
    },
  },

  section: {
    props: {
      title: "string" as Primitive,
      description: "string" as Primitive,
    },
  },

  /* ================================
     TABS
  ================================= */

  tabs: {
    props: {
      variant: ["line", "pills", "segmented"] as const,
      align: ["start", "center", "end"] as const,
      lazy: "boolean" as Primitive,
    },

    /*
      Tabs принимают обычные blocks.
      Каждый block становится вкладкой.

      tab.label = block.title
      tab.content = block
    */
  },

} as const
/* =========================
   ATOMIC UI
   ========================= */

export const Atom = {
  heading: {
    props: {
      text: "string" as Primitive,
      fallback: "string" as Primitive,
      level: [1, 2, 3, 4] as const,
    },
  },

  text: {
    props: {
      value: "string" as Primitive,
      muted: "boolean" as Primitive,
    },
  },

  divider: {
    props: {} as const,
  },

  spacer: {
    props: {
      size: "number" as Primitive,
    },
  },

  badge: {
    props: {
      label: "string" as Primitive,
      color: [
        "default",
        "success",
        "warning",
        "danger",
      ] as const,
      size: [
        "sm",
        "md",
        "lg",
      ] as const,
    },
  },
  link: {
  props: {
    label: "string" as Primitive,

    to: "string" as Primitive,

    external: "boolean" as Primitive,

    underline: "boolean" as Primitive,
    muted: "boolean" as Primitive,

    icon: "string" as Primitive,
  },
},

  insert_variables: {
    props: {
      source: "string" as Primitive,
      targetField: "string" as Primitive,
      title: "string" as Primitive,
      format: [
        "template",
        "raw",
        "dollar",
      ] as const,
    },
  },
} as const
/* =========================
   ACTIONS (SEMANTIC)
   ========================= */

export const Action = {
  action: {
    props: {
      label: "string",
      icon: "string",

      // 🔥 ЯВНОЕ РАЗДЕЛЕНИЕ
      to: "string",
      action: "string",

      ctx: "object",

      variant: ["primary", "secondary", "ghost", "danger"],
    },
  },


  

  upload: {
    props: {
      name: "string" as Primitive,
      label: "string" as Primitive,
      multiple: "boolean" as Primitive,
      upload_action: "string" as Primitive,
      commit_action: "string" as Primitive,
      files: "array" as Primitive,
      ctx: "object" as Primitive,
      refresh: "array" as Primitive,
      accept: "string" as Primitive,
      auto_commit: "boolean" as Primitive,
      disabled: "boolean" as Primitive,
    },
  },
 

} as const
/* =========================
   CONTENT (PAGE LEVEL)
   ========================= */

export const Content = {
custom: {
    props: {
      component: "string" as Primitive,
      props: "object" as Primitive,
    },
  },
form: {
  modes: {
    // =====================================================
    // ENTITY FORM (CRUD)
    // =====================================================
    entity: {
      entity: "string" as Primitive,

      "mode?": ["create", "edit", "view"] as const,
      "objectId?": "string" as Primitive,

      "initial?": "object" as Primitive,

      "submit?": {
        label: "string" as Primitive,
        action: "string" as Primitive,

        redirect: [
          "string",
          {
            to: "string" as Primitive,
            ctx: "object" as Primitive,
          },
        ] as const,

        closeModal: "boolean" as Primitive,
      },
    },

    // =====================================================
    // ACTION FORM
    // =====================================================
    action: {
      schema: "string" as Primitive,

      submit: [
        "string",
        {
          action: "string" as Primitive,
          label: "string" as Primitive,

          redirect: [
            "string",
            {
              to: "string" as Primitive,
              ctx: "object" as Primitive,
            },
          ] as const,

          closeModal: "boolean" as Primitive,
        },
      ] as const,

      "redirect?": [
        "string",
        {
          to: "string" as Primitive,
          ctx: "object" as Primitive,
        },
      ] as const,
    },
  },

  // =====================================================
  // 🔥 НОВЫЙ LAYOUT (ТОЛЬКО PRESET)
  // =====================================================
 formLayout: {
  preset: [
    "default",
    "two-columns",
    "single-column",
    "wide",
  ] as const,

  density: [
    "comfortable", // много воздуха
    "default",     // стандарт
    "compact",     // плотнее
    "dense",       // максимально плотно
  ] as const,
},
},


table: {
  props: {
    entity: "string" as Primitive,
    fieldset: "string" as Primitive,

    data: "any" as Primitive,

    filter: "object" as Primitive,

    searchableFields: "array" as Primitive,
    selectionActions: "array" as Primitive,

    rowClick: [
      "boolean",
      {
        to: "string" as Primitive,
        action: "string" as Primitive,

        params: "object" as Primitive,
        ctx: "object" as Primitive,

        confirm: [
          "boolean",
          {
            message: "string" as Primitive,
          },
        ] as const,
      },
    ] as const,

    to: "string" as Primitive,
  },

  features: {
    toolbar: "boolean" as Primitive,
    search: "boolean" as Primitive,
    selection: "boolean" as Primitive,
    rowClick: "boolean" as Primitive,
    rowActions: "boolean" as Primitive,
    visibleFields: "boolean" as Primitive,
  },

  toolbar: {
    actions: "array" as Primitive,
  },

  rowActions: "array" as Primitive,
  bulkActions: "array" as Primitive,
},

matrix: {
  props: {
    source: "string",   // code
    params: "object",   // ctx
  }
},
chat_thread: {
    props: {
      thread: "any" as Primitive,
      participants: "array" as Primitive,
      messages: "array" as Primitive,

      currentUserId: "string" as Primitive,

      reply: {
        schema: "string" as Primitive,

        submit: {
          action: "string" as Primitive,
          label: "string" as Primitive,

          redirect: [
            "string",
            {
              to: "string" as Primitive,
              ctx: "object" as Primitive,
            },
          ] as const,

          closeModal: "boolean" as Primitive,
        },

        ctx: "object" as Primitive,
      },

      features: {
        header: "boolean" as Primitive,
        participants: "boolean" as Primitive,
        timestamps: "boolean" as Primitive,
        grouping: "boolean" as Primitive,
        autoScroll: "boolean" as Primitive,
        realtime: "boolean" as Primitive,
        attachments: "boolean" as Primitive,
      },
    },
  },
 chat_list: {
  props: {
    data: "array",
    selectedId: "string",
    to: "string",
  },

  features: {
    unread: "boolean",
    timestamp: "boolean",
  },
},
document: {
  props: {

    /*
     * actions
     */

    openAction: "string" as Primitive,
    saveAction: "string" as Primitive,

    /*
     * target
     */

    objectId: "string" as Primitive,

    /*
     * runtime ctx
     */

    ctx: "object" as Primitive,

    /*
     * editor
     */

    editable: "boolean" as Primitive,

    autosave: "boolean" as Primitive,
    autosaveDelay: "number" as Primitive,

    /*
     * ui
     */

    toolbar: [
      "minimal",
      "compact",
      "full",
    ] as const,

    fullscreen: "boolean" as Primitive,

    /*
     * refresh integrations
     */

    refresh: "array" as Primitive,
  },

  features: {

    save: "boolean" as Primitive,
    autosave: "boolean" as Primitive,

    history: "boolean" as Primitive,

    upload: "boolean" as Primitive,
    export: "boolean" as Primitive,

    comments: "boolean" as Primitive,

    fullscreen: "boolean" as Primitive,
  },
},
} as const
export const Control = {
  if: {
    props: {
      when: "string" as Primitive,
    },
  },

 for: {
  props: {
    each: "string" as Primitive,
    range: "number" as Primitive,   // ⭐ NEW
    as: "string" as Primitive,
    index: "string" as Primitive, // 🔥 ДОБАВИТЬ

  },
},
} as const
export const Data = {
  resource: {
    props: {
      source: "string" as Primitive,
      params: "object" as Primitive,
      assign: "string" as Primitive,

      lazy: "boolean" as Primitive,
      watch: "array" as Primitive,
    },
  },
} as const
/* =========================
   ROOT REGISTRY
   ========================= */

export const Registry = {
  layout: Layout,
  block: Block,
  structural: Structural,
  atom: Atom,
  action: Action,
  content: Content,
  control: Control,
    data: Data,   // ⭐ ДОБАВИЛИ
} as const
