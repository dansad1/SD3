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

const UserFormPage = page(

  "user:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Пользователь"
          />

          <Text
            value="Создание и редактирование пользователя"
            muted
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Назад к списку"
            to="user:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="user"

          ctx={{
            id: "$query.id",
          }}

          fieldset="default"

          submit={{
            label: "Сохранить",
          }}

        

          formLayout={{

            preset: "single-column",

            density: "comfortable",

          }}

        />

      </Stack>

    </Section>

  </Container>
)

export default UserFormPage