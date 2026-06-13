/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Matrix,
  Action,
} from "@/framework"

const TicketSLAMatrixPage = page(
  "ticket_slas:matrix",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading
            level={1}
            text="SLA по типам заявок"
          />

          <Text
            value="Настройка времени SLA в часах по типам заявок и приоритетам"
            muted
          />
        </Stack>

        <Stack gap="sm">
          <Action
            label="← Назад"
            to="ticket:list"
            variant="secondary"
          />
        </Stack>

        <Matrix
          source="ticket-slas"
          params={{}}
        />

      </Stack>
    </Section>
  </Container>
)

export default TicketSLAMatrixPage