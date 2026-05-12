/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Table,
  Action,
} from "@/framework"

const DisciplineListPage = page(
  "discipline:list",

  <Container padding="lg">
    <Section>
      <Stack gap="lg">

        {/* Header */}
        <Stack gap="sm">
          <Heading level={1} text="Дисциплины" />
          <Text
            value="Управление дисциплинами учебного журнала"
            muted
          />
        </Stack>

        {/* Actions + Table */}
        <Stack gap="md">

          <Action
            label="Добавить дисциплину"
            to="discipline:form"   // ✅ FIX
            variant="primary"
          />

   <Table
  entity="discipline"
  fieldset="default"

  features={{
    search: true,
    selection: true,
    rowClick: true,
    rowActions: true,
  }}

  toolbar={{
    actions: ["reload", "fields"],
  }}

  rowActions={[
    {
      key: "edit",
      label: "Редактировать",
      variant: "secondary",
      to: "discipline:form",
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
        id: "$row.id",
      },
      confirm: {
        message: "Удалить эту дисциплину?",
      },
    },
  ]}
/>

        </Stack>

      </Stack>
    </Section>
  </Container>
)

export default DisciplineListPage