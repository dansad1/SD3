/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Split,
  Section,
  Stack,
  Heading,
  Text,
  Form,
  Spacer,
} from "@/framework"

const LoginPage = page(
  "login",

  <Container align="center" padding="lg" maxWidth="lg">
    <Split ratio="3:2" gap="lg" responsive>

      {/* LEFT */}
      <Stack gap="lg" variant="card">
        <Stack gap="sm">
          <Heading level={1} text="Электронный журнал" />
          <Heading
            level={3}
            text="Система учёта занятий и успеваемости"
          />
        </Stack>

        <Text
          value="Рабочий инструмент для старост, преподавателей и администрации учебных заведений."
          muted
        />

        <Spacer size={32} />

        <Text
          value="Доступен с компьютера и мобильных устройств."
          muted
        />
      </Stack>

      {/* RIGHT */}
      <Stack gap="lg">
        <Section title="Вход в систему">
          <Stack gap="md">

            <Text
              value="Используйте учётную запись вашего учебного заведения"
              muted
            />

            {/* ✅ ACTION FORM (как entity, но для login) */}
            <Form
              schema="auth.login"
              submit={{
                action: "auth.login",
                label: "Войти",
                redirect: {
      to: "journal:overview",
                },
              }}
            />

          </Stack>
        </Section>
      </Stack>

    </Split>
  </Container>
)

export default LoginPage