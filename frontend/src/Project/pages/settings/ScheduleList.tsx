/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Table,
  Action,
} from "@/framework"

const ScheduleListPage = page(

  "schedule:list",

  <Container
    maxWidth="xl"
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
            text="Расписания"
          />

          <Text
            value="Рабочие расписания сервисов"
            muted={true}
          />

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Action
          label="Создать расписание"
          to="schedule:form"
          variant="primary"
        />

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <Table

          entity="schedule"

          features={{

            toolbar: true,

            search: true,

            selection: false,

            rowClick: true,

            rowActions: true,

            visibleFields: true,

          }}

          rowClick={{

            to: "schedule:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {

              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "schedule:form",

              ctx: {
                id: "$row.id",
              },

            },

            {

              key: "delete",

              label: "Удалить",

              variant: "danger",

              action: "entity.delete",

              ctx: {
                entity: "schedule",
                id: "$row.id",
              },

              confirm: {
                message: "Удалить расписание?",
              },

            },

          ]}

        />

      </Stack>

    </Section>

  </Container>

)

export default ScheduleListPage