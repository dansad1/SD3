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
  Page_actions,

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
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* NAVIGATION */}
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

          submit={false}

          formLayout={{

            preset: "single-column",

            density: "comfortable",

          }}

        />

        {/* ===================================== */}
        {/* PAGE ACTIONS */}
        {/* ===================================== */}

        <Page_actions
          sticky
          align="right"
        >

          <Action

            label="Сохранить"

            action="form.submit"

            target="form:user:$query.id"

            variant="primary"

          />

        </Page_actions>

      </Stack>

    </Section>

  </Container>
)

export default UserFormPage