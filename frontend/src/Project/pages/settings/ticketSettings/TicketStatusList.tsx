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

const TicketStatusListPage = page(

  "ticket_status:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📊 Статусы заявок"
          />

          <Text
            value="Статусы управляют жизненным циклом и workflow заявок"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить статус"
            to="ticket_status:form"
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

          entity="ticket_statuses"

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

            to: "ticket_status:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "ticket_status:form",

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
                entity: "ticket-statuses",
                id: "$row.id",
              },

              confirm: {
                message:
                  "Удалить статус?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default TicketStatusListPage