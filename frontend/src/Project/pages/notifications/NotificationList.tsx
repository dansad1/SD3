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

const NotificationTemplateListPage = page(

  "notification_template:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="📨 Шаблоны уведомлений"
          />

          <Text
            value="Шаблоны используются правилами уведомлений для формирования сообщений."
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить шаблон"
            to="notification_template:form"
            variant="primary"
          />

          <Action
            label="← Обзор уведомлений"
            to="notification:overview"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* TABLE */}
        {/* ===================================== */}

        <Table

          entity="notification-templates"

          fieldset="default"

          features={{

            search: true,

            selection: true,

            rowClick: true,

            rowActions: true,

          }}

          toolbar={{

            actions: [

              "reload",

              "fields",

            ],

          }}

          rowClick={{

            to: "notification_template:form",

            ctx: {

              id: "$row.id",

            },

          }}

          rowActions={[

            {

              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "notification_template:form",

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

                entity: "notification-templates",

                id: "$row.id",

              },

              confirm: {

                message:
                  "Удалить шаблон уведомления?",

              },

            },

          ]}

        />

      </Stack>

    </Section>

  </Container>

)

export default NotificationTemplateListPage