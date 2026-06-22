/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Custom,
} from "@/framework"


const NotificationOverviewPage = page(

  "notification:overview",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        <Heading
          level={1}
          text="Уведомления — обзор"
        />

       <Custom
  component="NotificationOverview"
  props={{
    process: "$query.id",
  }}
/>
      </Stack>

    </Section>

  </Container>

)

export default NotificationOverviewPage