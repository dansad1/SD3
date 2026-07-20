/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Form,
} from "@/framework"

const ArticleFormPage = page(

  "article:form",

  <Container
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ================================= */}
        {/* HEADER                            */}
        {/* ================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Статья: $article.title"
            fallback="Новая статья"
          />
          <Text
            value="Создание и редактирование статьи базы знаний"
            variant="muted"
          />
        </Stack>
        {/* ================================= */}
        {/* FORM                              */}
        {/* ================================= */}

        <Form
          entity="article"
          objectId="$query.id"

          submit={{
            label: "Сохранить",
            redirect: {
              to: "article:list",
            },

          }}
          

        />
      </Stack>
    </Section>
  </Container>
)

export default ArticleFormPage