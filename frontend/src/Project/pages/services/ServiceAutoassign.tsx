/** @jsxImportSource @/framework/DSL/runtime */

import {
  page,
  Container,
  Section,
  Stack,
  Heading,
  Text,
  Matrix,
  Action,
  If,
} from "@/framework"

const ServiceAutoassignPage = page(

  "service:autoassign",

  <Container
    maxWidth="xl"
    padding="lg"
  >

    <Section>

      <Stack gap="lg">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Heading
            level={1}
            text="Автоназначение: $service.name"
            fallback="Автоназначение"
          />

         <Text
  value="Настройка автоматического назначения исполнителей, групп и наблюдателей"
  variant="muted"
/>

        </Stack>

        {/* ================================================= */}
        {/* ACTIONS */}
        {/* ================================================= */}

        <Stack gap="sm">

          <Action
            label="← Назад к сервису"
            to="service:form"
            variant="secondary"
            ctx={{
              id: "$query.service",
            }}
          />

        </Stack>

        {/* ================================================= */}
        {/* MATRIX */}
        {/* ================================================= */}

        <If when="$query.service">

          <Matrix

            source="service.autoassign"

            params={{

              service:
                "$query.service",

            }}

            features={{

              autosave: true,

              bulk: true,

            }}

          />

        </If>

      </Stack>

    </Section>

  </Container>

)

export default ServiceAutoassignPage