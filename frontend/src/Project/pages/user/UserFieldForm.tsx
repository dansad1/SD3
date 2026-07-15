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
  Timeline,
} from "@/framework"

const UserFieldFormPage = page(

  "userfield:form",

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
            text="Поле пользователя"
          />

          <Text
            value="Создание и редактирование поля пользователя"
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
            to="userfield:list"
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
              entity="user-fields"
              objectId="$query.id"
              submit={{
                label: "Сохранить",
                redirect: {
                  to: "userfields:list",
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
                  source="user-field.access"
                  params={{
                    field: "$query.id",
                  }}
                />

              </Stack>

            </Section>

          </If>

          {/* ================================= */}
          {/* HISTORY */}
          {/* ================================= */}

          <If when="$query.id">

            <Section title="История">

              <Timeline
                source="entity.history"
                params={{
                  entity: "user-fields",
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

export default UserFieldFormPage