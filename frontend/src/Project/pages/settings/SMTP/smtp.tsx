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

const EmailSettingsFormPage = page(
  "email-settings:form",

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
            text="📧 SMTP"
          />

          <Text
            value="Настройка исходящей почты"
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
            label="← Назад"
            to="settings:home"
            variant="secondary"
          />

          <Action
            label="Отправить тестовое письмо"
            action="email.send_test"
            variant="primary"
          />
        </Stack>

        {/* ===================================== */}
        {/* SINGLETON FORM */}
        {/* ===================================== */}

        <Form
          entity="email-settings"
          submit={{
            label: "Сохранить",
          }}
          formLayout={{
            preset: "two-columns",
            density: "comfortable",
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default EmailSettingsFormPage