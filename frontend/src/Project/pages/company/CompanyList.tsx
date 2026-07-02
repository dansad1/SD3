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

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Компании"
          />

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="Добавить компанию"
            to="company:form"
            variant="primary"
          />

        </Stack>

        {/* ================================================= */}
        {/* TABLE */}
        {/* ================================================= */}

        <Table
          entity="company"

          /*
            🔥 fieldset-driven columns
          */
          fieldset="default"

          /*
            🔥 built-in runtime features
          */
          features={{
            search: true,
            selection: true,
            rowClick: true,
            rowActions: true,
            sorting: true,
            pagination: true,
          }}

          /*
            🔥 semantic toolbar
          */
          toolbar={{
            actions: [
              "reload",
              "fields",
              "filters",
            ],
          }}

          /*
            🔥 row navigation
          */
          rowClick={{
            to: "company:form",
            ctx: {
              id: "$row.id",
            },
          }}

          /*
            🔥 semantic row actions
          */
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

              bulk: true,

              confirm: {
                message:
                  "Удалить выбранные компании?",
              },

              ctx: {
                entity: "company",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>

)

export default CompanyListPage