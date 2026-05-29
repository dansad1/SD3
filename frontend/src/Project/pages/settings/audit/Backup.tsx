/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Table,
  Action,
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
  value="Создание, загрузка, скачивание и восстановление резервных копий"
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
            search: true,
            selection: false,
            rowClick: false,
            rowActions: true,
            visibleFields: true,
          }}

          rowActions={[
            {
              key: "download_db",
              label: "DB",
              variant: "secondary",
              action: "backup.download.db",
              ctx: {
                id: "$row.id",
              },
            },

            {
              key: "download_media",
              label: "Media",
              variant: "secondary",
              action: "backup.download.media",
              ctx: {
                id: "$row.id",
              },
            },

            {
              key: "restore",
              label: "Восстановить",
              variant: "danger",
              action: "backup.restore",
              ctx: {
                id: "$row.id",
              },
              confirm: {
                message: "Восстановить систему из этого бэкапа?",
              },
            },
          ]}
        />

      </Stack>
    </Section>
  </Container>
)

export default BackupPage