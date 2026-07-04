/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Action,
  Custom,
} from "@/framework"

const TicketTypeSelectPage = page(

  "ticket:type_select",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ============================================= */}
        {/* HEADER */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Новая заявка"
          />

          <Text
            value="Выберите сервис и тип обращения"
            variant="muted"
            size="md"
            weight="regular"
          />

        </Stack>

        {/* ============================================= */}
        {/* ACTIONS */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Action
            label="← К списку заявок"
            to="ticket:list"
            variant="secondary"
          />

        </Stack>

        {/* ============================================= */}
        {/* SELECT */}
        {/* ============================================= */}

        <Custom
          component="TicketTypeSelect"
        />

      </Stack>

    </Section>

  </Container>

)

export default TicketTypeSelectPage