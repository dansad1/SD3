/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Table,
} from "@/framework"


const ErrorAuditPage = page(

  "audit:error",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        <Stack gap="sm">

          <Heading
            level={1}
            text="Ошибки системы"
          />

          <Text
            value="Необработанные исключения приложения"
            variant="muted"
          />

        </Stack>

        <Table

          entity="error-journal"

          rowVariant="accordion"

          features={{

            toolbar: true,

            search: true,

            selection: false,

            rowClick: false,

            rowActions: false,

            visibleFields: true,

            sorting: true,

          }}

        />

      </Stack>

    </Section>

  </Container>

)

export default ErrorAuditPage