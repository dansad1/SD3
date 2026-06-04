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

const TicketPriorityListPage = page(

  "ticket_priority:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="⚠️ Приоритеты заявок"
          />

          <Text
            value="Приоритеты определяют важность и порядок обработки заявок"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить приоритет"
            to="ticket_priority:form"
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

          entity="ticket_priorities"

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

            to: "ticket_priority:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "ticket_priority:form",

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
                entity: "ticket-priorities",
                id: "$row.id",
              },

              confirm: {
                message:
                  "Удалить приоритет?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default TicketPriorityListPage