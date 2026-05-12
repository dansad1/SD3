/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Action,
  Upload,
} from "@/framework"

const UsersImportPage = page(
  "users:import",

  <Container padding="lg" maxWidth="md">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading level={1} text="Импорт пользователей" />
          <Text
            value="Загрузите Excel файл для массового создания пользователей"
            muted
          />
        </Stack>

        <Action
          label="Скачать шаблон"
          action="user.import.template"
          variant="secondary"
        />

        <Upload
          name="file"
          label="Excel файл"

          upload_action="user.import.upload"
          commit_action="user.import.commit"

          multiple={false}
          accept=".xlsx"

          
        />

      </Stack>
    </Section>
  </Container>
)

export default UsersImportPage