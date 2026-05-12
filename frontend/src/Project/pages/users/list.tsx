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

const UsersListPage = page(
  "user:list",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        {/* Header */}
        <Stack gap="sm">
          <Heading level={1} text="Пользователи" />
          <Text
            value="Управление пользователями системы"
            muted
          />
        </Stack>

        <Stack gap="md">

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

          <Table
            entity="user"
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

                // ✅ navigation
                to: "user:form",
                ctx: {
                  id: "$row.id",
                },
              },
              {
                key: "delete",
                label: "Удалить",
                variant: "danger",

                // ✅ backend action
                action: "entity.delete",

                ctx: {
                  id: "$row.id",
                },

                confirm: {
                  message: "Удалить пользователя?",
                },
              },
            ]}
          />

        </Stack>

      </Stack>
    </Section>
  </Container>
)

export default UsersListPage