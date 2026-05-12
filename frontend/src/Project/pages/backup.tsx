/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Action,
  Upload,
  Table,
  Divider,
} from "@/framework"

const BackupPage = page(
  "backup:list",

  <Container maxWidth="xl" padding="lg">
    <Section>
      <Stack gap="lg">

        <Heading
          level={1}
          text="Резервные копии"
        />

        <Action
          label="♻️ Создать новый бэкап"
          action="backup.create"
          variant="primary"
        />

        <Divider />

        <Upload
          name="backup_file"
          label="📤 Загрузить бэкап (.zip)"
          accept=".zip"
          multiple={false}
          upload_action="backup.upload"
          auto_commit={true}
        />

        <Divider />

        <Table
          entity="backup"
          features={{
            toolbar: false,
            search: false,
            selection: false,
            rowClick: false,
            rowActions: true,
            visibleFields: false,
          }}
         rowActions={[
  {
    key: "download-db",
    label: "📄 Скачать базу данных",
    action: "backup.download.db",
    variant: "ghost",
    reloadOnSuccess: false,
    ctx: {
      id: "$row.name",
    },
  },
  {
    key: "download-media",
    label: "🖼 Скачать медиафайлы",
    action: "backup.download.media",
    variant: "ghost",
    reloadOnSuccess: false,
    ctx: {
      id: "$row.name",
    },
  },
  {
    key: "restore",
    label: "🔁 Восстановить",
    action: "backup.restore",
    variant: "danger",
    ctx: {
      id: "$row.name",
    },
    confirm: {
      message: "Восстановить этот бэкап?",
    },
  },
]}
        />

      </Stack>
    </Section>
  </Container>
)

export default BackupPage