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
  Action,
  If,
  Matrix,
} from "@/framework"


const TicketFieldFormPage = page(

  "ticket_field:form",

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
  text="Тип заявки: $ticket_field.name"
  fallback="Тип заявки"
/>

          <Text

            value="Создание и редактирование поля типа заявки"

            variant="muted"

            size="md"

            weight="regular"

          />

        </Stack>


        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ==================================== */}
        <Stack gap="sm">
          <Action            
          label="← Назад к типу заявки"
            to="ticket_type:form"

            ctx={{
              id:
                "$query.ticket_type",
            }}
            variant="secondary"
          />
        </Stack>

        {/* ===================================== */}
        {/* TABS */}
        {/* ===================================== */}
        <Tabs variant="line">

          {/* ================================= */}
          {/* MAIN */}
          {/* ================================= */}
          <Section title="Основное">
            <Form
              entity="ticket-field"
              objectId="$query.id"
              initial={{
                ticket_type:
                  "$query.ticket_type",
              }}
              submit={{
                label: "Сохранить",
                redirect: {
                  to:
                    "ticket_type:form",
                  ctx: {
                    id:"$query.ticket_type",
                  },
                },

              }}

              

            />

          </Section>


          {/* ================================= */}
          {/* ACCESS */}
          {/* ================================= */}
          <If when="$query.id">
            <Section title="Доступ">
              <Stack gap="md">

                <Matrix
                  source="ticket-field.access"
                  params={{
                    field:
                      "$query.id",

                  }}
                />
              </Stack>
            </Section>
          </If>
        </Tabs>
      </Stack>
    </Section>
  </Container>

)
export default TicketFieldFormPage