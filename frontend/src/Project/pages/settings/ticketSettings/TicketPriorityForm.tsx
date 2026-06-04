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
  text="⚠️ Приоритет заявки: $ticket_priorities.name"
  fallback="Новый приоритет заявки"
/>

          <Text
            value="Создание и редактирование приоритета заявки"
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
            to="ticket_priority:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* FORM */}
        {/* ===================================== */}

        <Form

          entity="ticket_priorities"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {
              to: "ticket_priority:list",
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

export default TicketPriorityFormPage