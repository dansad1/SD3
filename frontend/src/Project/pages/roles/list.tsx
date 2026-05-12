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

const RoleListPage = page(
  "role:list",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading level={1} text="Роли" />
          <Text
            value="Управление ролями и правами доступа в системе"
            muted
          />
        </Stack>

        <Stack gap="md">

          <Action
            label="Добавить роль"
            to="role:form"
            variant="primary"
          />

          <Table
            entity="role"
            fieldset="default"

            features={{
              search: true,
              selection: true,
              rowClick: true,
                  rowActions: true,
            }}

            toolbar={{
              actions: ["reload", "fields"],
            }}

            rowActions={[
              {
                key: "edit",
                label: "Редактировать",
                variant: "secondary",
                to: "role:form",
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
                  id: "$row.id",
                },
                confirm: {
                  message: "Удалить эту роль?",
                },
              },
            ]}
          />

        </Stack>

      </Stack>
    </Section>
  </Container>
)

export default RoleListPage