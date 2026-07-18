/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Action,
  Container,
  Heading,
  Section,
  Stack,
  Table,
  Text,
  Upload,
} from "@/framework"

const BackupPage = page(
  "backup:list",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Stack gap="sm">
          <Heading
            level={1}
            text="Резервные копии"
          />

          <Text
            value={
              "Создание, загрузка, скачивание, "
              + "восстановление и удаление резервных копий"
            }
            variant="muted"
          />
        </Stack>

        <Stack gap="sm">
          <Action
            label="Создать бэкап"
            action="backup.create"
            variant="primary"
          />

          <Upload
            name="file"
            label="Загрузить backup ZIP"
            upload_action="backup.upload"
            accept=".zip"
            auto_commit
            refresh={["backup:list"]}
          />
        </Stack>

        <Table
          entity="backup"
          features={{
            toolbar: true,
            search: false,
            selection: false,
            rowClick: false,
            rowActions: true,
            visibleFields: true,
          }}
          rowActions={[
            {
              key: "download_db",
              label: "Скачать БД",
              variant: "secondary",
              action: "backup.download.db",
              ctx: {
                id: "$row.id",
              },
            },
            {
              key: "download_media",
              label: "Скачать media",
              variant: "secondary",
              action: "backup.download.media",
              ctx: {
                id: "$row.id",
              },
            },
           {
  key: "restore",
  label: "Восстановить",
  variant: "secondary",
  action: "backup.restore",
  ctx: {
    id: "$row.id",
  },
  confirm: {
    message: (
      "Текущая база данных и media будут заменены "
      + "содержимым этой резервной копии. Продолжить?"
    ),
  },
},
            {
              key: "delete",
              label: "Удалить",
              variant: "danger",
              action: "backup.delete",
              ctx: {
                id: "$row.id",
              },
              confirm: {
                message: (
                  "Удалить резервную копию без "
                  + "возможности восстановления?"
                ),
              },
            },
          ]}
        />

      </Stack>
    </Section>
  </Container>
)

export default BackupPage