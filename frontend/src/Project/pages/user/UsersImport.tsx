/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Upload,
  Action,
  Link,
} from "@/framework"

const UsersImportPage = page(

  "users:import",

  <Container
    maxWidth="lg"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ============================================ */}
        {/* HEADER */}
        {/* ============================================ */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Импорт пользователей"
          />

          <Text
            value="Загрузите Excel (.xlsx). Система проверит файл, покажет ошибки и зарегистрирует пользователей."
            muted
          />

        </Stack>

        {/* ============================================ */}
        {/* ACTIONS */}
        {/* ============================================ */}

        <Stack gap="sm">

          <Action
            label="← Назад"
            to="user:list"
            variant="secondary"
          />

          <Link
            label="Скачать шаблон"
            to="/api/entity/user/template/"
            external
            variant="muted"
          />

        </Stack>

        {/* ============================================ */}
        {/* UPLOAD */}
        {/* ============================================ */}

        <Upload
          name="file"

          label="Файл Excel"

          accept=".xlsx"

          multiple={false}

          upload_action="users.import.preview"

          commit_action="users.import.commit"

          auto_commit={false}

          refresh={[
            "user.list",
          ]}
        />

      </Stack>

    </Section>

  </Container>

)

export default UsersImportPage