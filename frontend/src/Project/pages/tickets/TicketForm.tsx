/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Action,
  Form,
  Tabs,
  If,
} from "@/framework"

const TicketFormPage = page(

  "ticket:form",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ============================================= */}
        {/* HEADER */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Тикет №$ticket.id"
            fallback="Новая заявка"
          />

          <Text
            value="Создание и обработка обращения"
            variant="muted"
          />

        </Stack>

        {/* ============================================= */}
        {/* ACTIONS */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Action
            label="← К списку"
            to="ticket:list"
            variant="secondary"
          />

        </Stack>

        {/* ============================================= */}
        {/* CONTENT */}
        {/* ============================================= */}

        <Tabs variant="line">

          <Section title="Основное">

            <Form

              entity="tickets"

              objectId="$query.id"

              ctx={{

                service:
                  "$query.service",

                type:
                  "$query.type",

              }}

              submit={{

                label: "Сохранить",

                redirect: {

                  to: "ticket:list",

                },

              }}

            />

          </Section>

          <If when="$query.id">

            <Section title="Комментарии">

              {/* Потом Matrix или Custom */}

            </Section>

          </If>

          <If when="$query.id">

            <Section title="История">

              {/* Timeline */}

            </Section>

          </If>

          <If when="$query.id">

            <Section title="Вложения">

              {/* Attachments */}

            </Section>

          </If>

        </Tabs>

      </Stack>

    </Section>

  </Container>

)

export default TicketFormPage