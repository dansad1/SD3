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
  If,
  Upload,
  Text,
  Matrix,
} from "@/framework"

const PairFormPage = page(
  "pair:form",

  <Container padding="lg" maxWidth="xl">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Пара: $pair.discipline.label"
          fallback="Новая пара"
        />

        <Tabs variant="line">

          {/* ================= ОСНОВНОЕ ================= */}

          <Section title="Основное">
            <Stack gap="lg">

              <Form
                entity="pair"
                objectId="$query.id"
                formLayout={{
                  preset: "two-columns",
                  density: "compact",
                }}
                submit={{
                  label: "Сохранить",
                  redirect: {
                    to: "discipline:list",
                  },
                }}
              />

            </Stack>
          </Section>

          {/* ================= ДЕТАЛИ (ТОЛЬКО ЕСЛИ ЕСТЬ ID) ================= */}

          <If when="$query.id">

            {/* ---------- МАТЕРИАЛЫ ---------- */}

            <Section title="Материалы">
              <Stack gap="md">

                <Upload
                  name="files"
                  label="Загрузить материалы"
                  upload_action="material_upload"
                  commit_action="material_commit"
                  multiple
                  ctx={{
                    entity: "pair",
                    object_id: "$query.id",
                  }}
                />

                <Table
                  entity="pair_material"
                  filter={{
                    pair: "$query.id",
                  }}
                  features={{
                    search: true,
                    selection: true,
                    rowClick: true,
                    rowActions: true,
                  }}
                  rowClick={{
                    to: "pair_material:form",
                    ctx: {
                      id: "$row.id",
                    },
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
                        message: "Удалить материал?",
                      },
                    },
                  ]}
                />

              </Stack>
            </Section>

            {/* ---------- ПОСЕЩАЕМОСТЬ ---------- */}

          <Section title="Посещаемость и оценки">
  <Stack gap="md">

    {/* ===== СТАТУС ===== */}

    <If when="$pair.attendance_finalized">
      <Text value="🔒 Посещаемость финализирована" />
    </If>

    {/* ===== MATRIX ===== */}

    <Matrix
      source="attendance.pair"
      params={{
        pair_id: "$query.id",
      }}
    />

    {/* ===== ACTION ===== */}

    <If when="!$pair.attendance_finalized">
      <Action
        label="Финализировать посещаемость"
        action="attendance.finalize"
        variant="secondary"
        ctx={{
          pair_id: "$query.id",
        }}
      />
    </If>

  </Stack>
</Section>

          </If>

        </Tabs>

      </Stack>
    </Section>
  </Container>
)

export default PairFormPage