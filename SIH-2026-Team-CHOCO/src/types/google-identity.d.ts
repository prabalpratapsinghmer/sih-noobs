/* Google Identity Services (GIS) – global type shims.
 * Only the subset used by GoogleLogin.tsx is typed here. */

export {}

declare global {
  interface GoogleCredentialResponse {
    credential: string
    select_by: string
    clientId?: string
  }

  interface GoogleButtonConfig {
    theme?: 'outline' | 'filled_blue' | 'filled_black'
    size?: 'large' | 'medium' | 'small'
    width?: number | string
    shape?: 'rectangular' | 'pill' | 'circle' | 'square'
    text?: 'signin_with' | 'signup_with' | 'continue_with' | 'signin'
    logo_alignment?: 'left' | 'center'
    type?: 'standard' | 'icon'
  }

  interface GoogleAccountsId {
    initialize(config: {
      client_id: string
      callback: (response: GoogleCredentialResponse) => void
      auto_select?: boolean
      cancel_on_tap_outside?: boolean
    }): void
    renderButton(parent: HTMLElement, config: GoogleButtonConfig): void
    prompt(callback?: (notification: unknown) => void): void
    disableAutoSelect(): void
    revoke(hint: string, callback?: (done: { successful: boolean }) => void): void
  }

  interface Google {
    accounts: {
      id: GoogleAccountsId
    }
  }

  interface Window {
    google?: Google
  }
}
