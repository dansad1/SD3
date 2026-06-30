const themes = {
    default: () => import("./default"),
    bitrix: () => import("./Bitrix"),
} as const;

const theme =
    (import.meta.env.VITE_THEME ?? "default").toLowerCase();

const loader =
    themes[theme as keyof typeof themes];

if (!loader) {
    throw new Error(`Unknown theme: ${theme}`);
}

await loader();