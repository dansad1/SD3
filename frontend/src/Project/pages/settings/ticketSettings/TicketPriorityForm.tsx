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

const TicketPriorityFormPage = page(

  "ticket_priority:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="⚠️ Приоритет заявки"
          />

          <Text
            value="Создание и редактирование приоритета заявки"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Назад к списку"
            to="ticket_priority:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="ticket-priorities"

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

export default TicketPriorityFormPage