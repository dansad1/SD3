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

const TicketCategoryListPage = page(

  "ticket_category:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📂 Категории заявок"
          />

          <Text
            value="Категории используются для группировки и классификации заявок"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить категорию"
            to="ticket_category:form"
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

          entity="ticket-categories"

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

            to: "ticket_category:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "ticket_category:form",

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
                entity: "ticket-categories",
                id: "$row.id",
              },

              confirm: {
                message:
                  "Удалить категорию?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default TicketCategoryListPage