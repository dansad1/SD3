/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Table,
  Action,
} from "@/framework"

const CompanyListPage = page(

  "company:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ============================================= */}
        {/* HEADER */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Компании"
          />

        </Stack>

        {/* ============================================= */}
        {/* ACTIONS */}
        {/* ============================================= */}

        <Stack gap="sm">

          <Action
            label="Добавить компанию"
            to="company:form"
            variant="primary"
          />

        </Stack>

        {/* ============================================= */}
        {/* TABLE */}
        {/* ============================================= */}

        <Table
          entity="company"

          fieldset="default"

          features={{
            search: true,
            selection: true,
            rowClick: true,
            rowActions: true,
            visibleFields: true,
          }}

          toolbar={{
            actions: [
              "reload",
              "fields",
            ],
          }}

          rowClick={{
            to: "company:form",
            ctx: {
              id: "$row.id",
            },
          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "company:form",

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
                entity: "company",
                id: "$row.id",
              },

              confirm: {
                message: "Удалить компанию?",
              },
            },

          ]}
        />

        {/* ============================================= */}
        {/* TEST SIDEBAR */}
        {/* ============================================= */}

        {/* ============================================= */}
{/* LEFT SIDEBAR */}
{/* ============================================= */}

<Section
  title="Навигация"
  description="sidebar-left"
  layout={{
    area: "sidebar-left",
  }}
>
  <Stack gap="sm">

    <Heading
      level={3}
      text="Левый sidebar"
    />

    <Action
      label="Пункт 1"
      variant="secondary"
    />

    <Action
      label="Пункт 2"
      variant="secondary"
    />

  </Stack>
</Section>

{/* ============================================= */}
{/* RIGHT SIDEBAR */}
{/* ============================================= */}

<Section
  title="Фильтры"
  description="sidebar-right"
  layout={{
    area: "sidebar-right",
  }}
>
  <Stack gap="sm">

    <Heading
      level={3}
      text="Правый sidebar"
    />

    <Action
      label="Очистить"
      variant="secondary"
    />

  </Stack>
</Section>

<Section
  title="Сохранённые фильтры"
  description="ещё один блок справа"
  layout={{
    area: "sidebar-right",
  }}
>
  <Stack gap="sm">

    <Heading
      level={4}
      text="Второй блок"
    />

  </Stack>
</Section>

{/* ============================================= */}
{/* OVERLAY TEST */}
{/* ============================================= */}

<Section
  title="Overlay"
  description="пока просто проверяем сборку дерева"
  layout={{
    area: "overlay",
  }}
>
  <Stack gap="sm">

    <Heading
      level={3}
      text="Overlay Area"
    />

  </Stack>
</Section>
      </Stack>

    </Section>

  </Container>
)

export default CompanyListPage