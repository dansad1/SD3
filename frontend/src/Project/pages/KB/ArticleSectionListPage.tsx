/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Action,
  Container,
  Heading,
  Section,
  Stack,
  Table,
} from "@/framework"

const ArticleSectionListPage = page(
  "article-section:list",

  <Container
    maxWidth="xl"
    padding="lg"
  >
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading
            level={1}
            text="Разделы базы знаний"
          />

          <Action
            label="Создать раздел"
            to="article-section:form"
            variant="primary"
          />

          <Action
            label="К статьям"
            to="article:list"
            variant="secondary"
          />
        </Stack>

        <Table
          entity="article-section"
          features={{
            toolbar: true,
            search: true,
            selection: false,
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
            to: "article-section:form",
            ctx: {
              id: "$row.id",
            },
          }}
          rowActions={[
            {
              key: "edit",
              label: "Редактировать",
              variant: "secondary",
              to: "article-section:form",
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
                entity: "article-section",
                id: "$row.id",
              },
              confirm: {
                message: "Удалить раздел?",
              },
            },
          ]}
        />

      </Stack>
    </Section>
  </Container>
)

export default ArticleSectionListPage