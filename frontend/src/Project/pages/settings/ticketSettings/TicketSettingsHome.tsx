/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Menu,
  Link,
  Action,
} from "@/framework"

const TicketSettingsHomePage = page(

  "ticket_settings:home",

  <Container padding="lg">

    <Section>

      <Stack gap="lg">

        {/* ===================================== */}
        {/* HEADER */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="🎫 Настройки заявок"
          />

          <Text
  value="Управление типами, статусами, SLA и workflow заявок"

  variant="muted"

  size="md"

  weight="regular"
/>

        </Stack>

        {/* ===================================== */}
        {/* MENU */}
        {/* ===================================== */}

        <Menu
          orientation="vertical"
          variant="cards"
          gap="sm"
        >

          <Link
            label="📂 Типы заявок"
            to="/page/ticket_type:list"
            variant="menu"
          />

          <Link
            label="⚠️ Приоритеты"
            to="/page/ticket_priority:list"
            variant="menu"
          />

          <Link
            label="📊 Статусы"
            to="/page/ticket_status:list"
            variant="menu"
          />

          <Link
            label="⏱ Время выполнения"
            to="/page/ticket_slas:matrix"
            variant="menu"
          />

          <Link
            label="🔁 Переходы статусов"
            to="/page/ticket:workflow"
            variant="menu"
          />

          <Link
            label="👥 Группы исполнителей"
            to="/page/executor_group:list"
            variant="menu"
          />

          <Link
            label="📂 Категории заявок"
            to="/page/ticket_category:list"
            variant="menu"
          />

        </Menu>

        {/* ===================================== */}
        {/* BACK */}
        {/* ===================================== */}

        <Stack gap="sm">

          <Action
            label="← Назад к настройкам"
            to="settings:home"
            variant="secondary"
          />

        </Stack>

      </Stack>

    </Section>

  </Container>
)

export default TicketSettingsHomePage