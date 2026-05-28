/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Menu,
  Link,
} from "@/framework"

const SettingsHomePage = page(
  "settings:home",

  <Container maxWidth="lg" padding="lg">

    <Section>

      <Stack gap="lg">

        <Heading
          level={3}
          text="⚙ Центр настроек"
        />

        <Menu
          orientation="vertical"
          variant="cards"
          gap="sm"
        >

          <Link
            label="Настройки SMTP"
            to="/page/settings.smtp:form"
            variant="menu"
          />

          <Link
            label="Приём заявок по email"
            to="/page/settings.email_receiver:form"
            variant="menu"
          />

          <Link
            label="Шаблоны уведомлений"
            to="/page/notification_matrix:list"
            variant="menu"
          />

          <Link
            label="Импорт пользователей"
            to="/page/import_users:page"
            variant="menu"
          />

          <Link
            label="Журнал действий"
            to="/page/user_action_logs:list"
            variant="menu"
          />

          <Link
            label="Ошибки системы"
            to="/page/system_error_logs:list"
            variant="menu"
          />

          <Link
            label="Журнал входов"
            to="/page/audit:auth"
            variant="menu"
          />

          <Link
            label="Резервные копии"
            to="/page/backup:list"
            variant="menu"
          />

          <Link
            label="Поля пользователей"
            to="/page/userfield:list"
            variant="menu"
          />

          <Link
            label="Поля компаний"
            to="/page/company_field:list"
            variant="menu"
          />

          <Link
            label="Расписания"
            to="/page/schedule:list"
            variant="menu"
          />

          <Link
            label="Настройки заявок"
            to="/page/ticket_settings:home"
            variant="menu"
          />

        </Menu>

      </Stack>

    </Section>

  </Container>
)

export default SettingsHomePage