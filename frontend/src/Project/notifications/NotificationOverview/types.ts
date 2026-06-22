export interface NotificationEvent {
    code: string
    label: string
    group?: string

}


export interface NotificationRow {
    id: number
    label: string
    events: string[]
    statuses: string[]

}


export interface NotificationOverviewProps {
    events: NotificationEvent[]
    rows: NotificationRow[]

}