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
            text="📊 Статус заявки: $ticket_statuses.name"
            fallback="Новый статус заявки"
          />

          <Text
            value="Создание и редактирование статуса заявки"
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
            to="ticket_status:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="ticket_statuses"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {
              to: "ticket_status:list",
            },

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