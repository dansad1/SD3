/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Form,
  Action,
} from "@/framework"

const PairTemplateFormPage = page(
  "pair_template:form",

  <Container padding="lg" maxWidth="md">
    <Section>
      <Stack gap="lg">

        <Heading level={1} text="Шаблон пары" />

        <Form
          entity="pair_template"
          objectId="$query.id"
          submit={{
            label: "Сохранить",
            redirect: {
              to: "discipline:form",
              ctx: {
                discipline: "$query.discipline",
              },
            },
          }}
        />

        {/* ✅ ctx остаётся */}
        <Action
          action="pair_generate"
          label="Сгенерировать пары"
          ctx={{
            discipline: "$query.discipline"
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default PairTemplateFormPage