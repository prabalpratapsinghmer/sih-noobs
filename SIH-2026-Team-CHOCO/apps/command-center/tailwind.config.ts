import type { Config } from 'tailwindcss'
import sharedConfig from '../../packages/ui-kit/tailwind.config'

export default {
  presets: [sharedConfig],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
    "../../packages/ui-kit/src/**/*.{ts,tsx}"
  ],
} satisfies Config
