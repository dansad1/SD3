/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Resource,
  Chat_thread,
  Action,
} from "@/framework"

const MessageThreadPage = page(
  "message_thread:view",

  <Container maxWidth="xl" padding="none">
    <Section>
      <Stack gap="none">

        {/* 🔙 назад */}
        <Action
          to="/page/message_center"
          label="← Назад"
        />

        <Resource
          source="message.thread"
          params={{
            id: "$query.id",
          }}
          assign="thread"
        />

        <Chat_thread
          thread="$thread"
          participants="$thread.participants"
          messages="$thread.messages"
          currentUserId="$thread.current_user_id"

          reply={{
            schema: "message.reply",
            submit: {
              action: "message.reply",
              label: "Отправить",
            },
            ctx: {
              thread_id: "$thread.id",
            },
          }}

          features={{
            header: true,
            participants: true,
            timestamps: true,
            grouping: true,
            autoScroll: true,
            realtime: true,
          }}
        />

      </Stack>
    </Section>
  </Container>
)

export default MessageThreadPage