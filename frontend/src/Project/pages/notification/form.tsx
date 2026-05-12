/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
  Text,
  Insert_variables,
} from "@/framework"

const NotificationTemplateFormPage = page(
  "notification_template:form",

  <Container padding="lg" maxWidth="lg">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading
            level={1}
            text="Шаблон: $notification_template.name"
            fallback="Новый шаблон уведомления"
          />
          

          <Text
            value="Настройка email, push и системных уведомлений"
            muted
          />
        </Stack>

        {/* ✅ загружаем переменные */}
        

        {/* ✅ чистая форма */}
        <Form
         entity="notification_template"
  objectId="$query.id"
          formLayout={{
                  preset: "single-column",
                  density: "compact",
                }}
          submit={{
            label: "Сохранить",
            redirect: {
              to: "notification_template:list",
            },
          }}
        />

      </Stack>
      <Insert_variables
    source="notification_template:variables"
    targetField="body"
  />
    </Section>
  </Container>
)

export default NotificationTemplateFormPage