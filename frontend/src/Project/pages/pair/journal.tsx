/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Resource,
  Tabs,
  Table,
  Text,
  For,
} from "@/framework"

const JournalPage = page(
  "journal:overview",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Обзорный журнал"
        />

        <Resource
          source="journal.overview"
          assign="journal"
        />

        <Tabs>

          <For
            each="$journal"
            as="discipline"
          >
            <Section
              title="$discipline.discipline"
            >
              <Stack gap="md">

                <Text
                  value="Целевое значение: $discipline.target_value"
                />

                <Table
                  data="$discipline.rows"
                  features={{
                    toolbar: false,
                    search: false,
                    selection: false,
                    rowClick: true,
                    rowActions: false,
                  }}
                  to="/page/user:profile?id=$row.student_id"
                />

              </Stack>
            </Section>
          </For>

        </Tabs>

      </Stack>
    </Section>
  </Container>
)

export default JournalPage