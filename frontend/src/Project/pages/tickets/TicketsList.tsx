/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Table,
  Action,
} from "@/framework"

const TicketsListPage = page(

  "ticket:list",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Тикеты"
          />

          <Text
            value="Список обращений servicedesk"
            muted
          />

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="Создать тикет"
            to="ticket:form"
            variant="primary"
          />

        </Stack>

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <Table
          entity="tickets"

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
            sorting: true,
            pagination: true,
          }}

          /*
            🔥 semantic toolbar
          */
          toolbar={{
            actions: [
              "reload",
              "fields",
              "filters",
            ],
          }}

          /*
            🔥 row navigation
          */
          rowClick={{
            to: "ticket:form",
            ctx: {
              id: "$row.id",
            },
          }}

          /*
            🔥 semantic row actions
          */
          rowActions={[

            {
              key: "view",

              label: "Открыть",

              variant: "secondary",

              to: "ticket:form",

              ctx: {
                id: "$row.id",
              },
            },

            {
              key: "delete",

              label: "Удалить",

              variant: "danger",

              action: "entity.delete",

              bulk: true,

              confirm: {
                message:
                  "Удалить выбранные тикеты?",
              },

              ctx: {
                entity: "ticket",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>

)

export default TicketsListPage