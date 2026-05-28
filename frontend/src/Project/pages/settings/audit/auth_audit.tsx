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

const AuthAuditPage = page(

  "audit:auth",

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
            text="Журнал авторизации"
          />

          <Text
            value="Входы, выходы и ошибки авторизации"
            muted
          />

        </Stack>

        {/* ===================================== */}
        {/* TABLE */}
        {/* ===================================== */}

        <Table

          entity="auth-journal"

          features={{

            toolbar: true,

            search: true,

            selection: false,

            rowClick: false,

            rowActions: false,

            visibleFields: true,
          }}

        />

      </Stack>

    </Section>

  </Container>
)

export default AuthAuditPage