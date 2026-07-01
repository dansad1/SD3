/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Form,
  Action,
} from "@/framework"

const NotificationTemplateFormPage = page(

  "notification_template:form",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📨 Шаблон уведомления: $notification_templates.name"
            fallback="Новый шаблон уведомления"
          />

          <Text
            value="Создание и редактирование шаблона уведомления"
            variant="muted"
            size="md"
            weight="regular"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="← Назад к списку"
            to="notification_template:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="notification-templates"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {

              to: "notification_template:list",

            },

          }}

        />

      </Stack>

    </Section>

  </Container>

)

export default NotificationTemplateFormPage