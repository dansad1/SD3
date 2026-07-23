/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Action,
  Container,
  Form,
  Heading,
  Section,
  Stack,
} from "@/framework"

const ArticleSectionFormPage = page(
  "article-section:form",

  <Container
    maxWidth="xl"
    padding="lg"
  >
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Раздел базы знаний"
        />

        <Action
          label="Назад к разделам"
          to="article-section:list"
          variant="secondary"
        />

        <Form
          entity="article-section"
          objectId="$query.id"
          submit={{
            label: "Сохранить",
            redirect: {
              to: "article-section:list",
            },
          }}
          formLayout={{
            preset: "single-column",
            density: "comfortable",
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default ArticleSectionFormPage