/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Matrix,
} from "@/framework"

const NotificationOverviewPage = page(
  "notification:overview",

  <Container maxWidth="xl" padding="lg">

    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Уведомления — обзор"
        />

        <Matrix
          source="notification-overview"
        />

      </Stack>
    </Section>

  </Container>
)

export default NotificationOverviewPage