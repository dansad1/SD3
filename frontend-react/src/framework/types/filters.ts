export interface FilterField {
    id: number;
    label: string;
    type: string;
    operators: { value: string; label: string }[];
    choices?: { value: string; label: string }[];
    extra?: { has_from?: boolean; has_to?: boolean };
}

export interface SavedFilter {
    id: number;
    name: string;
    query: Record<string, string>;
}

export interface MetaResponse {
    fields: FilterField[];
    saved_filters: SavedFilter[];
    widget_map: Record<string, string>;
}
