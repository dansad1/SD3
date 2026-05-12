/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Tabs,
  Form,
  Table,
  Resource,
  For,
  Text,
} from "@/framework"

const UserProfilePage = page(
  "user:profile",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Пользователь: $user.username"
          fallback="Профиль пользователя"
        />

        <Tabs>

          {/* =========================
             TAB 1: ПРОФИЛЬ
          ========================= */}
          <Section title="Профиль">
            <Form
  entity="user"
  mode="edit"
  objectId="$me.id"
  submit={{
    label: "Сохранить",
    redirect: {
      to: "user:list",
    },
  }}
/>
          </Section>

          {/* =========================
             TAB 2: ЖУРНАЛ
          ========================= */}
          <Section title="Журнал">
            <Stack gap="lg">

              <Resource
                source="user.journal"
                assign="journal"
              />

              {/* 🔥 ВОТ ЭТО ТЫ ПРОПУСТИЛ */}
              <Tabs>

                <For each="$journal" as="discipline">
                  <Section title="$discipline.discipline">
                    <Stack gap="md">

                      <Text
                        value="Ожидаемая оценка: $discipline.target_value"
                      />

                      <Table
                        data="$discipline.rows"
                        features={{
                          toolbar: false,
                          search: false,
                          selection: false,
                          rowClick: false,
                          rowActions: false,
                        }}
                      />

                      <Text
                        value="Итоговая оценка: $discipline.current_grade"
                      />

                    </Stack>
                  </Section>
                </For>

              </Tabs>

            </Stack>
          </Section>

        </Tabs>

      </Stack>
    </Section>
  </Container>
)

export default UserProfilePage