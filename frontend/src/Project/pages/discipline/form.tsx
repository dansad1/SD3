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
  Action,
  Upload,
  If,
  For
} from "@/framework"

const DisciplineFormPage = page(
  "discipline:form",

  <Container padding="lg" maxWidth="xl">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Дисциплина: $discipline.name"
          fallback="Новая дисциплина"
        />

        <Tabs variant="line">

          <Section title="Основное">
            <Stack gap="lg">
              <Form
                entity="discipline"
                objectId="$query.id"
                submit={{
                  label: "Сохранить",
                  redirect: {
                    to: "discipline:list",
                  },
                }}
              />
            </Stack>
          </Section>
<If when="$query.id">

  <Section title="Сводка">

    <Stack gap="lg">

      <Resource
        source="journal.discipline.overview"

        params={{
          discipline_id: "$query.id",
        }}

        assign="overview"
      />

      <For
        each="$overview"
        as="discipline"
      >

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

        </Stack>

      </For>

    </Stack>

  </Section>

</If>
          <If when="$query.id">
            <Section title="Связанные пары">
              <Stack gap="md">

                <Action
                  label="Добавить пару"
                  variant="primary"
                  to="pair:form"
                  ctx={{
                    discipline: "$query.id",
                  }}
                />

                <Table
                  entity="pair"
                  filter={{
                    discipline: "$query.id",
                  }}
                  features={{
                    search: true,
                    selection: false,
                    rowClick: true,
                    rowActions: true,
                  }}
                  rowClick={{
                    to: "pair:form",
                    ctx: {
                      id: "$row.id",
                      discipline: "$query.id",
                    },
                  }}
                  rowActions={[
                    {
                      key: "edit",
                      label: "Редактировать",
                      variant: "secondary",
                      to: "pair:form",
                      ctx: {
                        id: "$row.id",
                        discipline: "$query.id",
                      },
                    },
                    {
                      key: "delete",
                      label: "Удалить",
                      variant: "danger",
                      action: "entity.delete",
                      ctx: {
                        entity: "pair",
                        id: "$row.id",
                      },
                      confirm: {
                        message: "Удалить пару?",
                      },
                    },
                  ]}
                />

              </Stack>
            </Section>
          </If>

      <If when="$query.id">
  <Section title="Шаблоны пар">
    <Stack gap="md">

      <Action
        label="Добавить шаблон"
        variant="primary"
        to="pair_template:form"
        ctx={{
          discipline: "$query.id",
        }}
      />
<Action
  label="Сгенерировать пары"
  action="pair_generate"
  ctx={{
    discipline: "$query.id"
  }}
/>
      <Table
        entity="pair_template"
        filter={{
          discipline: "$query.id",
        }}
        features={{
          search: true,
          selection: false,
          rowClick: true,
          rowActions: true,
        }}
        rowClick={{
          to: "pair_template:form",
          ctx: {
            id: "$row.id",
            discipline: "$query.id",
          },
        }}
        rowActions={[
          {
            key: "edit",
            label: "Редактировать",
            variant: "secondary",
            to: "pair_template:form",
            ctx: {
              id: "$row.id",
              discipline: "$query.id",
            },
          },
          {
            key: "delete",
            label: "Удалить",
            variant: "danger",
            action: "entity.delete",
            ctx: {
              entity: "pair_template",
              id: "$row.id",
            },
            confirm: {
              message: "Удалить шаблон пары?",
            },
          },
        ]}
      />

    </Stack>
  </Section>
</If>

          <If when="$query.id">
            <Section title="Файлы дисциплины">
              <Stack gap="md">

                <Upload
                  name="materials"
                  label="Загрузить файлы"
                  upload_action="material_upload"
                  commit_action="material_commit"
                  multiple
                  ctx={{
                    entity: "discipline",
                    object_id: "$query.id",
                  }}
                />

                <Table
                  entity="pair_material"
                  filter={{
                    discipline: "$query.id",
                  }}
                  features={{
                    rowActions: true,
                  }}
                  rowActions={[
                    {
                      key: "open",
                      label: "Открыть",
                      variant: "secondary",
                      href: "$row.file_url",
                      target: "_blank",
                    },
                    {
                      key: "delete",
                      label: "Удалить",
                      variant: "danger",
                      action: "entity.delete",
                      ctx: {
                        entity: "pair_material",
                        id: "$row.id",
                      },
                      confirm: {
                        message: "Удалить этот файл?",
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

export default DisciplineFormPage