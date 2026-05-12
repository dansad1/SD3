/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Split,
  Stack,
  Resource,
  Chat_list,
  Chat_thread,
} from "@/framework"

const MessageCenterPage = page(
  "message_center",

  <Container maxWidth="xl" padding="lg">
    <Section>

      <Split ratio="320px 1fr" gap="md">

        {/* 🔹 SIDEBAR */}
        <Stack gap="sm">
          <Resource
            source="message.center"
            assign="threads"
          />

          <Chat_list
            data="$threads"
            to="/page/message_center?id=$item.id"
          />
        </Stack>

        {/* 🔹 CHAT */}
        <Stack gap="sm">
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

      </Split>

    </Section>
  </Container>
)

export default MessageCenterPage