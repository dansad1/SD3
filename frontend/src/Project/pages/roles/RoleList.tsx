/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Table,
  Action,
  If,
} from "@/framework"

const RoleListPage = page(

  "role:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        <Stack gap="sm">

          <Heading
            level={1}
            text="Роли"
          />

        </Stack>

        <Stack gap="md">

          <If
            when="${can['role.create']}"
          >

            <Action
              label="Добавить роль"
              to="roles:form"
              variant="primary"
            />

          </If>

          <Table

            entity="roles"

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

            rowActions={[

              {
                key: "edit",

                label: "Редактировать",

                variant: "secondary",

                to: "roles:form",

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

                  entity: "roles",

                  id: "$row.id",

                },

                confirm: {
                  message: "Удалить эту роль?",
                },
              },

            ]}
          />

        </Stack>

      </Stack>

    </Section>

  </Container>
)

export default RoleListPage