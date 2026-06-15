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
  Tabs,
  If,
  Timeline,
} from "@/framework"

const TicketPriorityFormPage = page(

  "ticket_priority:form",

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
            text="⚠️ Приоритет заявки: $ticket_priorities.name"
            fallback="Новый приоритет заявки"
          />

          <Text
            value="Создание и редактирование приоритета заявки"
            variant="muted"
            size="md"
            weight="regular"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="← Назад к списку"
            to="ticket_priority:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* CONTENT */}
        {/* ===================================== */}

        <Tabs variant="line">

          {/* ===================================== */}
          {/* MAIN */}
          {/* ===================================== */}

          <Section title="Основное">

            <Stack gap="lg">

              <Form

                entity="ticket_priorities"

                objectId="$query.id"

                submit={{

                  label: "Сохранить",

                  redirect: {
                    to: "ticket_priority:list",
                  },

                }}

                formLayout={{

                  preset: "single-column",

                  density: "comfortable",

                }}

              />

            </Stack>

          </Section>

          {/* ===================================== */}
          {/* HISTORY */}
          {/* ===================================== */}

          <If when="$query.id">

            <Section title="История">

              <Timeline

                source="entity.history"

                params={{

                  entity:
                    "ticket_priorities",

                  id:
                    "$query.id",

                }}

              />

            </Section>

          </If>

        </Tabs>

      </Stack>

    </Section>

  </Container>

)

export default TicketPriorityFormPage