/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Link,
  Custom,
} from "@/framework"


const NotificationOverviewPage = page(

  "notification:overview",

  <Container
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        <Heading
          level={1}
          text="Уведомления — обзор"
        />

        <Link
          to="/page/notification_template:list"
          label="Перейти к списку уведомлений"
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