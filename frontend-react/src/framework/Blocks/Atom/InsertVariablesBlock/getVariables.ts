import { api } from "@/framework/api/client"

export type VariableItem = {
  key: string
  label: string
  value: string
}

export type VariableGroup = {
  key: string
  label: string
  items: VariableItem[]
}

export type VariablesResponse = {
  title?: string
  groups?: VariableGroup[]
}

export function getVariables(source: string) {
  return api.get<VariablesResponse>(
    `/resource/${source}/`
  )
}