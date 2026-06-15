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

const ArticleListPage = page(

  "article:list",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        <Stack gap="sm">

          <Heading
            level={1}
            text="База знаний"
          />

        </Stack>

        <Stack gap="md">

          <Action
            label="Создать статью"
            to="article:form"
            variant="primary"
          />

          <Table

            entity="article"

            features={{

              search: true,

              selection: false,

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

              to: "article:form",

              ctx: {
                id: "$row.id",
              },

            }}

            rowActions={[

              {
                key: "edit",

                label: "Редактировать",

                variant: "secondary",

                to: "article:form",

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

                  entity: "article",

                  id: "$row.id",

                },

                confirm: {
                  message: "Удалить статью?",
                },
              },

            ]}
          />

        </Stack>

      </Stack>

    </Section>

  </Container>
)

export default ArticleListPage