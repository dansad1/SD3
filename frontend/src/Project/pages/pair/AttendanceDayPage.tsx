/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Matrix,
} from "@/framework"

const AttendanceDayPage = page(
  "attendance:day_summary",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading text="Сводка дня" />

        <Matrix
          source="attendance.day"
          params={{
            date: "$query.date",
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default AttendanceDayPage