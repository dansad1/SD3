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

const NotificationTemplateListPage = page(
  "notification_template:list",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading
            level={1}
            text="Шаблоны уведомлений"
          />

          <Text
            value="Управление шаблонами email, push и системных уведомлений"
            muted
          />
        </Stack>

        <Stack gap="md">

          {/* ✅ CREATE */}
          <Action
            label="Новый шаблон"
            to="notification_template:form"
            variant="primary"
          />

          {/* ✅ TABLE */}
          <Table
            entity="notification_template"
            fieldset="default"
            features={{
              search: true,
              selection: true,
              rowClick: true,
            }}
            toolbar={{
              actions: ["reload", "fields"],
            }}
            rowActions={[
              {
                key: "edit",
                label: "Редактировать",
                variant: "secondary",
                to: "notification_template:form",
                params: {
                  id: "$row.id",
                },
              },
              {
                key: "delete",
                label: "Удалить",
                variant: "danger",
                confirm: {
                  message: "Удалить шаблон уведомления?",
                },
              },
            ]}
          />

        </Stack>

      </Stack>
    </Section>
  </Container>
)

export default NotificationTemplateListPage