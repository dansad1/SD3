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

const CompanyFormPage = page(

  "company:form",

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
            text="Компания: $company.name"
            fallback="Новая компания"
          />

            <Text
  value="Создание и редактирование компании"

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
            label="← Назад к списку"
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

          <Section title="Основные">

            <Stack gap="lg">

              <Form

                entity="company"

                ctx={{
                  id: "$query.id",
                  fieldset: "$query.fieldset",
                }}

                submit={{

                  label: "Сохранить",

                  redirect: {
                    to: "company:list",
                  },

                }}

                formLayout={{

                  preset: "single-column",

                  density: "comfortable",

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
                  to="user:form"
                  ctx={{
                    company: "$query.id",
                  }}
                />

                <Table

                  entity="user"

                  filter={{
                    company: "$query.id",
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

                      label: "Удалить из компании",

                      variant: "danger",

                      action: "company.user.remove",

                      ctx: {
                        company: "$query.id",
                        user: "$row.id",
                      },

                      confirm: {
                        message:
                          "Удалить пользователя из компании?",
                      },
                    },

                  ]}

                />

              </Stack>

            </Section>

          </If>

          {/* ============================================= */}
          {/* DEPARTMENTS */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Отделы">

              <Stack gap="md">

                <Action
                  label="Создать отдел"
                  variant="primary"
                  to="department:form"
                  ctx={{
                    company: "$query.id",
                  }}
                />

                <Table

                  entity="department"

                  filter={{
                    company: "$query.id",
                  }}

                  features={{
                    search: true,
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
                          "Удалить отдел?",
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

export default CompanyFormPage