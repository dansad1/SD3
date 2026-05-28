/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Stack,
  Heading,
  Text,
  Form,
  Action,
} from "@/framework"

const ForgotPasswordPage = page(

  "forgot-password",

  {

    auth: false,

    guestOnly: true,

    chrome: {

      mode: "auth",

      navbar: false,

      sidebar: false,

      footer: false,

      fullscreen: true,
    },
  },

  <Container
    maxWidth="sm"
    padding="lg"
  >

    <Stack
      gap="lg"
      variant="card"
    >

      <Heading
        level={1}
        text="Сброс пароля"
      />

      <Text
        value="Введите email"
        variant="muted"
      />

      <Form

        schema="password.reset.request"

        submit={{

          action:
            "password.reset.request",

          label:
            "Отправить ссылку",
        }}

        formLayout={{
          preset: "single-column",
        }}

      />

      <Action
        label="Назад ко входу"
        to="/page/login"
        variant="ghost"
      />

    </Stack>

  </Container>
)

export default ForgotPasswordPage