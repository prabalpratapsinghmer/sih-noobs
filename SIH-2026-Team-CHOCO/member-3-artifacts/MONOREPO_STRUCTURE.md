# Monorepo Structure

> npm/pnpm workspaces. One repo, four frontends, one shared package, devops folder.
> See `ENV.md` for variables, `DEVOPS.md` for containers, `UI_KIT_API.md` for the shared package.

---

## 1. Root Tree

```
sih26184/
├── apps/
│   ├── frontend-victim/      # Victim Portal → M4, port 3000
│   ├── frontend-admin/       # Admin Panel → me, port 3001
│   ├── frontend-field/       # Field Dashboard → me, port 3002
│   └── frontend-command/     # Command Center → me, port 3003
├── packages/
│   └── ui-kit/               # @sih/ui shared design system
├── devops/
│   ├── docker/               # Dockerfiles + nginx.Dockerfile + nginx.conf
│   ├── compose/              # docker-compose.yml
│   ├── k8s/                  # manifests/, configmaps/, minikube-setup.sh
│   ├── ci/                   # Jenkinsfile + .github/workflows/ci.yml
│   ├── monitoring/           # prometheus.yml + grafana dashboards JSON
│   ├── logging/              # docker-compose.elk.yml + filebeat.yml
│   └── scripts/              # compose-up.sh, demo-prep.sh
├── .env.example              # all env vars committed
├── .github/                  # GitHub Actions workflow
├── docs/                     # API-CONTRACTS.md, STACK.md, UI-KIT-API.md
└── package.json              # workspace root
```

---

## 2. Root `package.json`

```json
{
  "name": "sih26184",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev":         "concurrently \"npm run dev -w apps/frontend-admin\" \"npm run dev -w apps/frontend-field\" \"npm run dev -w apps/frontend-command\"",
    "dev:admin":   "npm run dev -w apps/frontend-admin",
    "dev:field":   "npm run dev -w apps/frontend-field",
    "dev:command": "npm run dev -w apps/frontend-command",
    "dev:victim":  "npm run dev -w apps/frontend-victim",
    "build":       "npm run build -w packages/ui-kit && npm run build --workspaces --if-present",
    "build:admin": "npm run build -w apps/frontend-admin",
    "build:field": "npm run build -w apps/frontend-field",
    "build:command":"npm run build -w apps/frontend-command",
    "typecheck":   "npm run typecheck --workspaces --if-present",
    "lint":        "eslint apps/*/src packages/*/src",
    "test":        "vitest run",
    "test:watch":  "vitest",
    "clean":       "rm -rf node_modules apps/*/node_modules packages/*/node_modules"
  },
  "devDependencies": {
    "concurrently": "^9.0.0",
    "eslint": "^9.0.0",
    "typescript": "^5.5.0",
    "vitest": "^2.0.0"
  }
}
```

---

## 3. Per-App `package.json` (example: Command Center)

```json
{
  "name": "@sih/command",
  "private": true,
  "scripts": {
    "dev":       "vite --port 3003",
    "build":     "tsc --noEmit && vite build",
    "typecheck": "tsc --noEmit",
    "lint":      "eslint src/",
    "preview":   "vite preview --port 3003"
  },
  "dependencies": {
    "@sih/ui": "workspace:*",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0",
    "@reduxjs/toolkit": "^2.0.0",
    "react-redux": "^9.0.0",
    "axios": "^1.7.0",
    "leaflet": "^1.9.0",
    "react-leaflet": "^4.0.0",
    "leaflet.heat": "^0.2.0",
    "leaflet.markercluster": "^1.5.0",
    "d3": "^7.0.0",
    "recharts": "^2.12.0",
    "framer-motion": "^11.0.0",
    "react-hook-form": "^7.53.0",
    "zod": "^3.23.0",
    "@hookform/resolvers": "^3.9.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/leaflet": "^1.9.0",
    "@types/d3": "^7.0.0",
    "vite": "^6.0.0",
    "typescript": "^5.5.0",
    "tailwindcss": "^4.0.0",
    "eslint": "^9.0.0"
  }
}
```

---

## 4. `@sih/ui` Package

See `UI_KIT_API.md` for the full public surface. Key build:

```json
{
  "name": "@sih/ui",
  "version": "0.1.0",
  "private": true,
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## 5. TypeScript Config (shared base)

```json
// tsconfig.base.json (at repo root)
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@sih/ui": ["packages/ui-kit/src"],
      "@sih/ui/*": ["packages/ui-kit/src/*"]
    }
  },
  "exclude": ["node_modules", "dist", "build"]
}
```

Each app extends this with `"extends": "../../tsconfig.base.json"` and adds its own `include`/`paths`.

---

## 6. Vite Config (per app)

```typescript
// apps/frontend-command/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@sih/ui': path.resolve(__dirname, '../../packages/ui-kit/src'),
    },
  },
  server: {
    port: 3003,
    proxy: {
      '/api': 'http://localhost:8000',
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

---

## 7. Scripts

### `devops/scripts/compose-up.sh`
```bash
#!/bin/bash
set -e
cp -n .env.example .env 2>/dev/null || true
docker compose -f devops/compose/docker-compose.yml up --build -d
echo "✅ Stack running at http://localhost"
echo "   Victim:  /"
echo "   Admin:   /admin"
echo "   Field:   /field"
echo "   Command: /command"
```

### `devops/scripts/demo-prep.sh`
```bash
#!/bin/bash
set -e
echo "🔨 Building all frontends..."
npm run build
echo "🐳 Building Docker images..."
docker compose -f devops/compose/docker-compose.yml build
echo "🚀 Starting stack..."
docker compose -f devops/compose/docker-compose.yml up -d
echo "🏥 Waiting for health checks..."
sleep 10
echo "✅ Demo ready at http://localhost"
```
