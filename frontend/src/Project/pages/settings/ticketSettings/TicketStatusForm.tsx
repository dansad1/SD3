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

const TicketStatusFormPage = page(

  "ticket_status:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📊 Статус заявки"
          />

          <Text
            value="Создание и редактирование статуса заявки"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Назад к списку"
            to="ticket_status:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="ticket-statuses"

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

export default TicketStatusFormPage