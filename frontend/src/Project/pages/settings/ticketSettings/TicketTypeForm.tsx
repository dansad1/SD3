/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Tabs,
  Form,
  Table,
  Action,
  If,
} from "@/framework"

const TicketTypeFormPage = page(
  "ticket_type:form",
  <Container
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
            text="Тип заявки"
            fallback="Новый тип заявки"
          />
          <Text
            value="Создание и настройка типа заявки"
            variant="muted"
          />
        </Stack>
        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}
        <Stack gap="sm">

          <Action
            label="← Назад к списку"
            to="ticket_type:list"
            variant="secondary"
          />
        </Stack>
        {/* ================================================= */}
        {/* TABS */}
        {/* ================================================= */}
        <Tabs variant="line">
          {/* ============================================= */}
          {/* MAIN */}
          {/* ============================================= */}
          <Section title="Основное">
            <Stack gap="lg">
              <Form
                entity="ticket-type"
                objectId="$query.id"
                submit={{
                  label: "Сохранить",
                  redirect: {
                    to: "ticket_type:list",
                  },
                }}
                
              />
            </Stack>
          </Section>

          {/* ============================================= */}
          {/* FIELDS */}
          {/* ============================================= */}
          <If when="$query.id">
            <Section title="Поля">
              <Stack gap="md">
                <Action
                  label="Добавить поле"
                  variant="primary"
                  to="ticket_field:form"
                  ctx={{
                    ticket_type: "$query.id",
                    back: "ticket_type:form",
                  }}
                />
                <Table
                  entity="ticket-field"
                  filter={{
                    ticket_type: "$query.id",

                  }}

                  features={{
                    search: true,
                    selection: false,
                    rowClick: true,
                    rowActions: true,

                  }}
                  rowClick={{
                    to: "ticket_field:form",
                    ctx: {
                      id: "$row.id",

                      ticket_type: "$query.id",

                      back: "ticket_type:form",
                    },
                  }}
                  rowActions={[
                    {
                      key: "edit",
                      label: "Редактировать",
                      variant: "secondary",
                      to: "ticket_field:form",

                      ctx: {
                        id: "$row.id",
                        ticket_type: "$query.id",
                        back: "ticket_type:form",
                      },
                    },
                    {
                      key: "delete",
                      label: "Удалить",
                      variant: "danger",
                      action: "entity.delete",
                      ctx: {
                        entity: "ticket-field",
                        id: "$row.id",

                      },
                      confirm: {
                        message: "Удалить поле?",
                      },
                    },
                  ]}
                />
              </Stack>
            </Section>
          </If>
        </Tabs>
      </Stack>
    </Section>
  </Container>

)

export default TicketTypeFormPage