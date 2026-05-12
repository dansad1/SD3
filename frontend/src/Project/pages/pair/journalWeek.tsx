/** @jsxImportSource @/framework/DSL/runtime */

import {
  Custom,
  page,
  
} from "@/framework"

const JournalWeekPage = page(
  "journal:week",
  <Custom
  component="JournalPrint"
  props={{
    mode: "week", // или "month"
    week_offset: "$query.week_offset"
  }}
/>
)

export default JournalWeekPage