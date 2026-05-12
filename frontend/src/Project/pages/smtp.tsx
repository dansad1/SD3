/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
  Action,
} from "@/framework"

const EmailSettingsPage = page(
  "email_settings:form",

  <Container maxWidth="md" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="SMTP настройки"
        />

        <Form
          entity="email_settings"
          objectId="$query.id"
          formLayout={{
            preset: "two-columns",
            density: "default",
          }}
          submit={{
            label: "Сохранить",
          }}
        />

        <Action
          label="Проверить SMTP"
          action="email_settings.test"
          variant="primary"
        />

      </Stack>
    </Section>
  </Container>
)

export default EmailSettingsPage