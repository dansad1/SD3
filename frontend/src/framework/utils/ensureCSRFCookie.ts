import { getCSRFToken } from "./csrf"

let csrfRequest: Promise<void> | null = null


export async function ensureCSRFCookie(): Promise<void> {
  if (getCSRFToken()) {
    return
  }

  if (!csrfRequest) {
    csrfRequest = fetch(
      "/api/csrf/",
      {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      },
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `CSRF initialization failed: ${response.status}`,
          )
        }
      })
      .finally(() => {
        csrfRequest = null
      })
  }

  await csrfRequest
}