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

const UserFieldFormPage = page(

  "userfield:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Поле пользователя"
          />

         <Text
  value="Создание и редактирование поля пользователя"

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
            label="Назад к списку"
            to="userfield:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

      <Form
  entity="user-fields"

  objectId="$query.id"

  submit={{
    label: "Сохранить",

    redirect: {
      to: "userfields:list",
    },
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

export default UserFieldFormPage