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

const UserFieldsListPage = page(
  "userfield:list",
  <Container padding="lg">
    <Section>
      <Stack gap="lg">
        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}
        <Stack gap="sm">
          <Heading
            level={1}
            text="Поля пользователей"
          />
        </Stack>
        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}
        <Stack gap="sm">
          <Action
            label="Добавить поле"
            to="userfield:form"
            variant="primary"
          />
        </Stack>
        {/* ===================================== */}
        {/* TABLE */}
        {/* ===================================== */}
        <Table
          entity="user-fields"
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
            to: "userfield:form",
            ctx: {
              id: "$row.id",
            },
          }}

          rowActions={[
            {
              key: "edit",
              label: "Редактировать",
              variant: "secondary",
              to: "userfield:form",
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
                entity: "user-fields",
                id: "$row.id",
              },
              confirm: {
                message: "Удалить поле?",
              },
            },

          ]}
        />
      </Stack>
    </Section>
  </Container>
)
export default UserFieldsListPage