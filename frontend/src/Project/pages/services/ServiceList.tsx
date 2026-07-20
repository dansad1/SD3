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
const ServiceListPage = page(
  "service:list",
  <Container
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
            text="Сервисы"
          />
            <Text
  value="Список сервисов"

  variant="muted"

  size="md"

  weight="regular"
/>
        </Stack>
        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="Создать сервис"
            to="service:form"
            variant="primary"
          />
        </Stack>
        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}
        <Table
          entity="service"
          features={{
            toolbar: true,
            search: true,
            selection: false,
            rowClick: true,
            rowActions: true,
            visibleFields: true,
          }}
          rowClick={{
            to: "service:form",
            ctx: {
              id: "$row.id",
            },
          }}
          rowActions={[
            {
              key: "edit",
              label: "Редактировать",
              variant: "secondary",
              to: "service:form",
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
                entity: "service",
                id: "$row.id",
              },
              confirm: {
                message: "Удалить сервис?",
              },
            },
          ]}
        />
      </Stack>
    </Section>
  </Container>

)

export default ServiceListPage