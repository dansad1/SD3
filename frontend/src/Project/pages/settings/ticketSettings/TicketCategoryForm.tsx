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

const TicketCategoryFormPage = page(

  "ticket_category:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📂 Категория заявки"
          />

          <Text
            value="Создание и редактирование категории заявки"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Назад к списку"
            to="ticket_category:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="ticket-categories"

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

export default TicketCategoryFormPage