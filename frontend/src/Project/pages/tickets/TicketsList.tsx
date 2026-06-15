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

        <Stack gap="sm">
          <Action
            label="Создать тикет"
            to="ticket:form"
            variant="primary"
          />
        </Stack>

        <Table
          entity="tickets"
          fieldset="default"

          features={{
            toolbar: true,
            search: true,
            selection: true,
            rowClick: true,
            rowActions: true,
            visibleFields: true,
          }}

          toolbar={{
            actions: [
              "reload",
              "fields",
            ],
          }}

          rowClick={{
            to: "ticket:form",
            ctx: {
              id: "$row.id",
            },
          }}

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
              ctx: {
                entity: "tickets",
                id: "$row.id",
              },
              confirm: {
                message: "Удалить тикет?",
              },
            },
          ]}
        />

      </Stack>
    </Section>
  </Container>
)

export default TicketsListPage