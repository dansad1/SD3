/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
} from "@/framework"

const BroadcastFormPage = page(
  "broadcast:form",

  <Container maxWidth="lg" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Создать рассылку"
        />

        <Form
          schema="broadcast.create"
          submit={{
            action: "broadcast.create",
            label: "Отправить",
            redirect: "/page/message_center",
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default BroadcastFormPage