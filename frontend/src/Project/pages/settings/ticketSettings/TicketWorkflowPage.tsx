/** @jsxImportSource @/framework/DSL/runtime */

import {
    page,
    Container,
    Stack,
    Heading,
    Text,
    Status_flow,
} from "@/framework"


const TicketWorkflowPage = page(

    "ticket:workflow",

    <Container padding="lg">

        <Stack gap="md">

            <Heading
                level={1}
                text="Переходы статусов"
            />

            <Text
                value="Настройка workflow заявок"
                muted
            />

            <Status_flow

                source="ticket.workflow"

                editable

            />

        </Stack>

    </Container>

)

export default TicketWorkflowPage