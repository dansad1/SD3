/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
} from "@/framework"

const UserFormPage = page(
  "user:form",

  <Container maxWidth="md" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Пользователь: $user.username"
          fallback="Новый пользователь"
        />

        <Form
          entity="user"
          objectId="$query.id"
          formLayout={{
    preset: "two-columns",
            density: "default", // 👈 теперь явно
          }}
          submit={{
            label: "Сохранить",
            redirect: "user:list",
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default UserFormPage