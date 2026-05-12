/** @jsxImportSource @/framework/DSL/runtime */

import {
  Custom,
  page,
  
} from "@/framework"

const JournalMonthPage = page(
  "journal:month",
  <Custom
  component="JournalPrint"
  props={{
    mode: "month", // или "month"
    week_offset: "$query.week_offset"
  }}
/>
)

export default JournalMonthPage