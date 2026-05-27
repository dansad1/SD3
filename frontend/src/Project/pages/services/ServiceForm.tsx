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

const ServiceFormPage = page(
  "service:form",
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
            text="Сервис: $service.name"
            fallback="Новый сервис"
          />
             <Text
  value="Настройка сервисов категорий и маршрутизации"

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
            to="service:list"
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
                entity="service"
                ctx={{
                  id: "$query.id",
                  parent: "$query.parent",

                }}
                submit={{
                  label: "Сохранить",

                  redirect: {
                    to: "service:list",
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
          {/* SUBSERVICES */}
          {/* ============================================= */}
          <If when="$query.id">

            <Section title="Подсервисы">
              <Stack gap="md">

                <Action
                  label="Создать подсервис"
                  variant="primary"
                  to="service:form"

                  ctx={{
                    parent: "$query.id",
                  }}

                />

                <Table
                  entity="service"
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
                      key: "delete",
                      label: "Удалить",
                      variant: "danger",
                      action: "entity.delete",
                      ctx: {
                        entity: "service",
                        id: "$row.id",
                      },
                      confirm: {
                        message: "Удалить подсервис?",
                      },
                    },
                  ]}
                />

              </Stack>

            </Section>

          </If>

          {/* ============================================= */}
          {/* USERS */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Пользователи">

              <Table

                entity="user"

                filter={{
                  services: "$query.id",
                }}

                features={{

                  search: true,

                  selection: false,

                  rowClick: true,

                  rowActions: false,

                }}

                rowClick={{

                  to: "user:form",

                  ctx: {
                    id: "$row.id",
                  },

                }}

              />

            </Section>

          </If>

          {/* ============================================= */}
          {/* COMPANIES */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Компании">

              <Table

                entity="company"

                filter={{
                  services: "$query.id",
                }}

                features={{

                  search: true,

                  selection: false,

                  rowClick: true,

                  rowActions: false,

                }}

                rowClick={{

                  to: "company:form",

                  ctx: {
                    id: "$row.id",
                  },

                }}

              />

            </Section>

          </If>

          {/* ============================================= */}
          {/* CATEGORIES */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Категории">

              <Table

                entity="ticket-category"

                filter={{
                  services: "$query.id",
                }}

                features={{

                  search: true,

                  selection: false,

                  rowClick: true,

                  rowActions: false,

                }}

                rowClick={{

                  to: "ticket_category:form",

                  ctx: {
                    id: "$row.id",
                  },

                }}

              />

            </Section>

          </If>

          {/* ============================================= */}
          {/* ASSIGNMENT RULES */}
          {/* ============================================= */}

          <If when="$query.id">

            <Section title="Правила назначения">

              <Stack gap="md">

                <Action

                  label="Создать правило"

                  variant="primary"

                  to="service:autoassign"

                  ctx={{
                    service: "$query.id",
                  }}

                />

                <Table

                  entity="category_assignment_rule"

                  filter={{
                    service: "$query.id",
                  }}

                  features={{

                    search: false,

                    selection: false,

                    rowClick: true,

                    rowActions: true,

                  }}

                  rowClick={{

                    to: "category_assignment_rule:form",

                    ctx: {
                      id: "$row.id",
                    },

                  }}

                  rowActions={[

                    {

                      key: "edit",

                      label: "Редактировать",

                      variant: "secondary",

                      to: "category_assignment_rule:form",

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
                        entity: "category_assignment_rule",
                        id: "$row.id",
                      },

                      confirm: {
                        message: "Удалить правило?",
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

export default ServiceFormPage