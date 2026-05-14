/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Table,
  Action,
} from "@/framework"

const UsersListPage = page(

  "user:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Пользователи"
          />

          

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="Добавить пользователя"
            to="user:form"
            variant="primary"
          />

          <Action
            label="Импорт пользователей"
            to="users:import"
            variant="secondary"
          />

        </Stack>

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <Table
          entity="user"

          /*
            🔥 fieldset-driven columns
          */
          fieldset="default"

          /*
            🔥 built-in runtime features
          */
          features={{
            search: true,
            selection: true,
            rowClick: true,
            rowActions: true,
          }}

          /*
            🔥 semantic toolbar
          */
          toolbar={{
            actions: [
              "reload",
              "fields",
            ],
          }}

          /*
            🔥 row navigation
          */
          rowClick={{
            to: "user:form",
            ctx: {
              id: "$row.id",
            },
          }}

          /*
            🔥 semantic row actions
          */
          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "user:form",

              ctx: {
                id: "$row.id",
              },
            },

            {
              key: "delete",

              label: "Удалить",

              variant: "danger",

              action: "entity.delete",

              ctx: {
                entity: "user",
                id: "$row.id",
              },

              confirm: {
                message: "Удалить пользователя?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default UsersListPage