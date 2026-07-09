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

const TicketFormPage = page(

  "ticket:form",

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
            text="Тикет №$ticket.id"
            fallback="Новая заявка"
          />

          <Text
            value="Создание и обработка обращения"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="← К списку"
            to="ticket:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form
          entity="tickets"

          objectId="$query.id"

          ctx={{
            service: "$query.service",
            type: "$query.type",
          }}

          submit={{
            label: "Сохранить",

            redirect: {
              to: "ticket:list",
            },
          }}
        />

      </Stack>

    </Section>

  </Container>

)

export default TicketFormPage