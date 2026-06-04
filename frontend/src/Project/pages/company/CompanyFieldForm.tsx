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

const CompanyFieldFormPage = page(

  "company_field:form",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Поле компании: $company_field.name"
            fallback="Новое поле компании"
          />

          <Text
            value="Создание и редактирование поля компании"
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
            label="← Назад к списку"
            to="company_field:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="company-fields"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {
              to: "company_field:list",
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

export default CompanyFieldFormPage