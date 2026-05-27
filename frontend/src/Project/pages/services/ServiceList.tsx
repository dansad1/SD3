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

const ServiceListPage = page(

  "service:list",

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
            text="Сервисы"
          />

          <Text
            value="Каталог сервисов и правил маршрутизации"
            muted={true}
          />

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="Создать сервис"
            to="service:form"
            variant="primary"
          />

        </Stack>

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <Table

          entity="service"


          features={{

            toolbar: true,

            search: true,

            selection: false,

            rowClick: true,

            rowActions: true,

            visibleFields: true,

          }}

          rowClick={{

            to: "service:form",

            ctx: {
              id: "$row.id",
            },

          }}

          rowActions={[

            {

              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "service:form",

              ctx: {
                id: "$row.id",
              },

            },

            {

              key: "create-child",

              label: "Создать подсервис",

              variant: "primary",

              to: "service:form",

              ctx: {
                parent: "$row.id",
              },

            },

            {

              key: "delete",

              label: "Удалить",

              variant: "danger",

              action: "entity.delete",

              ctx: {
                entity: "service",
                id: "$row.id",
              },

              confirm: {
                message: "Удалить сервис?",
              },

            },

          ]}

        />

      </Stack>

    </Section>

  </Container>

)

export default ServiceListPage