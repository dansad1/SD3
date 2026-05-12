/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Resource,
  Table,
} from "@/framework"

const BroadcastViewPage = page(
  "broadcast:view",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Рассылка"
        />

        <Resource
          source="broadcast.detail"
          params={{
            id: "$query.id",
          }}
          assign="broadcast"
        />

        <Table
          data="$broadcast.recipients"
          features={{
            toolbar: false,
            search: false,
            selection: false,
            rowClick: false,
            rowActions: false,
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default BroadcastViewPage