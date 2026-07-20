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

const DepartmentFormPage = page(

  "department:form",

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
            text="Отдел: $department.name"
            fallback="Новый отдел"
          />

             <Text
  value="Создание и редактирование отдела"

  variant="muted"

  size="md"

  weight="regular"
/>

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="← Назад к компаниям"
            to="company:list"
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

  entity="department"

  objectId="$query.id"

  submit={{

    label: "Сохранить",

    redirect: {
      to: "company:form",

      ctx: {
        id: "$form.company",
      },
    },

  }}

  

/>

            </Stack>

          </Section>

          {/* ============================================= */}
          {/* USERS */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Пользователи">

              <Stack gap="md">

                <Action
                  label="Добавить пользователя"
                  variant="primary"
                  action="department.user.add.modal"
                  ctx={{
                    department: "$query.id",
                  }}
                />

                <Table

                  entity="user"

                  filter={{
                    departments: "$query.id",
                  }}

                  features={{
                    search: true,
                    selection: false,
                    rowClick: true,
                    rowActions: true,
                  }}

                  rowClick={{
                    to: "user:form",

                    ctx: {
                      id: "$row.id",
                    },
                  }}

                  rowActions={[

                    {
                      key: "edit",

                      label: "Редактировать",

                      variant: "secondary",

                      to: "user:form",

                      ctx: {
                        id: "$row.id",
                      },
                    },

                    {
                      key: "remove",

                      label: "Удалить из отдела",

                      variant: "danger",

                      action: "department.user.remove",

                      ctx: {
                        department: "$query.id",
                        user: "$row.id",
                      },

                      confirm: {
                        message:
                          "Удалить пользователя из отдела?",
                      },
                    },

                  ]}

                />

              </Stack>

            </Section>

          </If>

          {/* ============================================= */}
          {/* SUBDEPARTMENTS */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Подотделы">

              <Stack gap="md">

                <Action
                  label="Создать подотдел"
                  variant="primary"

                  to="department:form"

                  ctx={{
                    company: "$form.company",
                    parent: "$query.id",
                  }}
                />

                <Table

                  entity="department"

                  filter={{
                    parent: "$query.id",
                  }}

                  features={{
                    search: false,
                    selection: false,
                    rowClick: true,
                    rowActions: true,
                  }}

                  rowClick={{
                    to: "department:form",

                    ctx: {
                      id: "$row.id",
                    },
                  }}

                  rowActions={[

                    {
                      key: "edit",

                      label: "Редактировать",

                      variant: "secondary",

                      to: "department:form",

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
                        entity: "department",
                        id: "$row.id",
                      },

                      confirm: {
                        message:
                          "Удалить подотдел?",
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

export default DepartmentFormPage