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

const TicketTypeListPage = page(

  "ticket_type:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📂 Типы заявок"
          />

          <Text
            value="Типы определяют workflow, SLA и поведение заявок"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить тип"
            to="ticket_type:form"
            variant="primary"
          />

          <Action
            label="← Назад к настройкам"
            to="ticket_settings:home"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* TABLE */}
        {/* ===================================== */}

        <Table

          entity="ticket-types"

          fieldset="default"

          features={{

            search: true,

            selection: true,

            rowClick: true,

            rowActions: true,

          }}

          toolbar={{
            actions: [
              "reload",
              "fields",
            ],
          }}

          rowClick={{

            to: "ticket_type:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "ticket_type:form",

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
                entity: "ticket-types",
                id: "$row.id",
              },

              confirm: {
                message:
                  "Удалить тип заявки?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default TicketTypeListPage