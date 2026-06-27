/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Form,
  Action,
} from "@/framework"

const ScheduleFormPage = page(

  "schedule:form",

  <Container
    maxWidth="lg"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Расписание: $schedule.name"
            fallback="Новое расписание"
          />

          <Text
            value="Настройка рабочего расписания"
            variant="muted"
          />

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Action
          label="← Назад к списку"
          to="schedule:list"
          variant="secondary"
        />

        {/* ================================================= */}
        {/* FORM */}
        {/* ================================================= */}

        <Form

          entity="schedule"

          objectId="$query.id"

          submit={{

            label: "Сохранить",

            redirect: {
              to: "schedule:list",
            },

          }}


        />

      </Stack>

    </Section>

  </Container>

)

export default ScheduleFormPage