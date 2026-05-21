/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,

  Container,
  Stack,
  Heading,
  Text,

  Form,
  Link,

  Page_actions,
  Action,

} from "@/framework"

const LoginPage = page(

  "login",

  {
    chrome: {
      mode: "auth",

      navbar: false,
      sidebar: false,

      fullscreen: true,
    },
  },

  <Container
    maxWidth="sm"
    padding="lg"
  >

    <Stack
      gap="xl"
      variant="card"
      size="md"
      align="stretch"
    >

      {/* ===================================== */}
      {/* HEADER */}
      {/* ===================================== */}

      <Stack
        gap="md"
        align="center"
      >

        <Stack
          gap="sm"
          align="center"
        >

          <Heading
            level={1}
            text="ServiceDesk"
          />

          <Text
            value="Войдите в систему"
            variant="muted"
            size="lg"
            weight="medium"
            align="center"
          />

        </Stack>

      </Stack>

      {/* ===================================== */}
      {/* FORM */}
      {/* ===================================== */}

      <Form

        schema="login"

        submit={false}

        formLayout={{

          preset: "single-column",

          density: "comfortable",

        }}

      />

      {/* ===================================== */}
      {/* ACTIONS */}
      {/* ===================================== */}

      <Page_actions
        sticky
        align="right"
      >

       <Action

  label="Войти"

  action="form.submit"

  target="action-form:login"

  variant="primary"

/>
      </Page_actions>

      {/* ===================================== */}
      {/* LINKS */}
      {/* ===================================== */}

      <Stack
        gap="sm"
        align="start"
      >

        <Link
          label="Забыли пароль?"
          to="/reset-password"
          variant="muted"
          underline="hover"
        />

        <Link
          label="Регистрация"
          to="/register"
          variant="muted"
          underline="hover"
        />

      </Stack>

    </Stack>

  </Container>
)

export default LoginPage