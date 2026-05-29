export interface FilterOption {
    value: string;
    label: string;
}

export interface FilterField {

    id: number;

    label: string;

    type: string;

    operators: FilterOption[];

    options?: FilterOption[];

    extra?: {
        has_from?: boolean;
        has_to?: boolean;
    };
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
