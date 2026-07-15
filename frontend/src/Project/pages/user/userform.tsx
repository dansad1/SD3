/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Form,
  Action,
  Tabs,
  If,
  Timeline,
} from "@/framework"

const UserFormPage = page(

  "user:form",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Пользователь: $user.login"
            fallback="Новый пользователь"
          />

          <Text
            value="Создание и редактирование пользователя"
            variant="muted"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Назад к списку"
            to="user:list"
            variant="secondary"
          />

        </Stack>

        {/* ===================================== */}
        {/* CONTENT */}
        {/* ===================================== */}

        <Tabs variant="line">

          <Section title="Основное">

            <Stack gap="lg">

              <Form
                entity="user"
                objectId="$query.id"
                submit={{
                  label: "Сохранить",
                  redirect: {
                    to: "user:list",
                  },
                }}
              />

            </Stack>

          </Section>

          <If when="$query.id">

            <Section title="История">

              <Timeline
                source="entity.history"
                params={{
                  entity: "user",
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

export default UserFormPage