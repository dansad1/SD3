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
  For,
  Resource,
} from "@/framework"

const SchedulePage = page(
  "schedule:week",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        {/* ================= HEADER ================= */}

        <Stack gap="sm">
          <Heading level={1} text="Расписание занятий" />
          <Text value="Учебное расписание" muted />
        </Stack>

        {/* ================= WEEK NAVIGATION ================= */}

        <Stack gap="sm">

          <Action
            label="← Предыдущая неделя"
            action="schedule.change_week"
            ctx={{ delta: -1 }}
          />

          <Action
            label="Текущая неделя"
            variant="primary"
            action="schedule.set_week"
            ctx={{ week_offset: 0 }}
          />

          <Action
            label="Следующая неделя →"
            action="schedule.change_week"
            ctx={{ delta: 1 }}
          />

        </Stack>
<Stack  gap="sm">

 <Action
  label="📘 Журнал посещаемости за неделю"
  variant="primary"
  to="journal:week"
  ctx={{
    week_offset: "$query.week_offset",
  }}
/>

<Action
  label="📗 Журнал месяца"
  variant="primary"
  to="journal:month"
  ctx={{
    week_offset: "$query.week_offset",
  }}
/>

</Stack>
        {/* ================= DATA ================= */}

        <Resource
          source="schedule.by_week"
          params={{
            week_offset: "$query.week_offset",
          }}
          assign="schedule"
          watch={["$query.week_offset"]}
        >

          <For each="$schedule.days" as="day">

            <Section title="$day.label">

              <Stack gap="md">

                {/* ===== СВОДКА ДНЯ ===== */}

                <Action
                  label="📝 Сводка дня"
                  variant="secondary"
                  to="attendance:day_summary"
                  ctx={{
                    date: "$day.date",
                  }}
                />

                {/* ===== ДОБАВИТЬ ПАРУ ===== */}

                <Action
                  label="➕ Добавить пару"
                  variant="primary"
                  to="pair:form"
                  ctx={{
                    date: "$day.date",
                  }}
                />

                {/* ===== СПИСОК ПАР ===== */}

                <Table
                  data="$day.pairs"
                  
                  features={{
                    search: false,
                    selection: false,
                    rowClick: true,
                  }}
                  rowClick={{
                    to: "pair:form",
                    params: {
                      id: "$row.id",
                    },
                  }}
                  rowActions={[
                    {
                      key: "edit",
                      label: "Редактировать",
                      variant: "secondary",
                      to: "pair:form",
                      params: {
                        id: "$row.id",
                      },
                    },
                    {
                      key: "delete",
                      label: "Удалить",
                      variant: "danger",
                      action: "pair.delete",
                      params: {
                        id: "$row.id",
                      },
                      confirm: {
                        message: "Удалить эту пару?",
                      },
                    },
                  ]}
                />

              </Stack>

            </Section>

          </For>

        </Resource>

      </Stack>
    </Section>
  </Container>
)

export default SchedulePage