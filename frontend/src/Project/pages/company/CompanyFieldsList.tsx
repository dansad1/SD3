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

const CompanyFieldsListPage = page(

  "company_field:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Поля компаний"
          />

        </Stack>

        {/* ===================================== */}
        {/* ACTIONS */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="Добавить поле"
            to="company_field:form"
            variant="primary"
          />

        </Stack>

        {/* ===================================== */}
        {/* TABLE */}
        {/* ===================================== */}

        <Table

          entity="company-fields"

          fieldset="default"

          features={{
            search: true,
            selection: true,
            rowClick: true,
            rowActions: true,
          }}

          toolbar={{
            actions: [
              "reload",
              "fields",
            ],
          }}

          rowClick={{
            to: "company_field:form",

            ctx: {
              id: "$row.id",
            },
          }}

          rowActions={[

            {
              key: "edit",

              label: "Редактировать",

              variant: "secondary",

              to: "company_field:form",

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
                entity: "company-fields",
                id: "$row.id",
              },

              confirm: {
                message: "Удалить поле?",
              },
            },

          ]}
        />

      </Stack>

    </Section>

  </Container>
)

export default CompanyFieldsListPage