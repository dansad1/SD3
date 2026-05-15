/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Form,
} from "@/framework"

const RoleFormPage = page(

  "roles:form",

  <Container
    padding="lg"
    maxWidth="md"
  >

    <Section>

      <Stack gap="lg">

        {/* ================================= */}
        {/* HEADER                            */}
        {/* ================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Роль"
          />

          <Text
            value="Создание и редактирование роли"
            muted
          />

        </Stack>

        {/* ================================= */}
        {/* FORM                              */}
        {/* ================================= */}

        <Form

          entity="roles"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {
              to: "roles:list",
            },

          }}

        />

      </Stack>

    </Section>

  </Container>
)

export default RoleFormPage