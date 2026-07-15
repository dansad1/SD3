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

const CompanyFieldFormPage = page(
"company_field:form",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">
        <Stack gap="sm">
          <Heading
            level={1}
            text="Поле компании: $company_field.name"
            fallback="Новое поле компании"
          />

      <Text
        value="Создание и редактирование поля компании"
        variant="muted"
        size="md"
        weight="regular"
      />
    </Stack>

    <Stack gap="sm">
      <Action
        label="← Назад к списку"
        to="company_field:list"
        variant="secondary"
      />
    </Stack>

    <Tabs variant="line">
      <Section title="Основное">
        <Form
          entity="company-fields"
          objectId="$query.id"
          submit={{
            label: "Сохранить",
            redirect: {
              to: "company_field:list",
            },
          }}
        />
      </Section>

      <If when="$query.id">
        <Section title="Доступ">
          <Stack gap="md">
            <Matrix
              source="company-field.access"
              params={{
                field: "$query.id",
              }}
            />
          </Stack>
        </Section>
      </If>

      <If when="$query.id">
        <Section title="История">
          <Timeline
            source="entity.history"
            params={{
              entity: "company-fields",
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

export default CompanyFieldFormPage
