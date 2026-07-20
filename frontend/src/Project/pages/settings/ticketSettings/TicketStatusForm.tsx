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

const TicketStatusFormPage = page(

  "ticket_status:form",

  <Container
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
            text="📊 Статус заявки: $ticket_statuses.name"
            fallback="Новый статус заявки"
          />

          <Text
            value="Создание и редактирование статуса заявки"
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
            to="ticket_status:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* CONTENT */}
        {/* ===================================== */}

        <Tabs variant="line">

          <Section title="Основное">

            <Stack gap="lg">

              <Form
                entity="ticket_statuses"
                objectId="$query.id"
                submit={{
                  label: "Сохранить",
                  redirect: {
                    to: "ticket_status:list",
                  },
                }}
              />

            </Stack>

          </Section>

          <If when="$query.id">

            <Section title="История">

              <Timeline
                source="entity.history"
                params={{
                  entity: "ticket_statuses",
                  id: "$query.id",
                }}
              />

            </Section>

          </If>

        </Tabs>

      </Stack>

    </Section>

  </Container>

)

export default TicketStatusFormPage