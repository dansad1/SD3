/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
} from "@/framework"

const RoleFormPage = page(
  "role:form",

  <Container padding="lg" maxWidth="md">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Роль: $role.name"
          fallback="Новая роль"
        />

        <Form
          entity="role"
          objectId="$query.id"
          submit={{
            label: "Сохранить",
            redirect: {
              to: "role:list",
            },
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default RoleFormPage