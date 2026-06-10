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


      </Stack>

    </Section>

  </Container>
)

export default CompanyListPage