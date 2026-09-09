# Authentication & Role-Based Access Control

> Auth flow: Member 2 owns the backend. Member 3 implements the frontend guards and token handling.
> See `API_CONTRACTS.md` §2 for the exact endpoint shapes.

---

## 1. Login Flows

### Police/Admin Login
- Input: Government ID + password.
- Endpoint: `POST /api/auth/login`.
- Returns: `access_token`, `refresh_token`, `user` object.
- Stored: `access_token` and `refresh_token` in `localStorage` (see §3).
- Session duration: 4 hours for officers, 8 hours for admins.

### Victim Login (Member 4)
- Input: Phone number + OTP.
- Endpoint: `POST /api/auth/victim/otp/request` → `POST /api/auth/victim/otp/verify`.
- Session duration: 2 hours.
- Not in Member 3's scope, but consumes the same `@sih/ui` auth primitives.

---

## 2. Role Definitions

| Role | Label | Access | Apps |
|------|-------|--------|------|
| `admin` | System Admin | Full access to all features, user management | Admin Panel + all |
| `inspector` | Cybercrime Inspector | Command Center, all complaints, LLM agent, actions | Command Center |
| `constable` | Police Constable | Field Dashboard, assigned alerts, limited complaints | Field Dashboard |
| `victim` | Complaint Victim | Own complaint + status only | Victim Portal (M4) |

---

## 3. Token Handling

### Storage
```typescript
// localStorage keys
'access'   → JWT access token (short-lived: 4h or 8h)
'refresh'  → JWT refresh token (long-lived: 7d)
```

**Trade-off note:** `localStorage` is used for this demo so refresh works across tabs. In production, use `HttpOnly` cookies (XSS-proof).

### Axios Interceptors (in `@sih/ui`)

The shared HTTP client handles:
1. **Request interceptor:** Attaches `Authorization: Bearer <access_token>` to every request.
2. **Response interceptor:** On 401, attempts one refresh via `POST /api/auth/refresh`.
3. If refresh succeeds: retries the original request transparently.
4. If refresh fails: clears tokens, emits `auth.expired`, routes to `/login`.

### Token Refresh Logic
```
Request → 401 Unauthorized
         → Try refresh with stored refresh_token
         → If refresh succeeds:
              Store new access_token
              Retry original request
         → If refresh fails:
              Clear localStorage
              Emit "auth.expired"
              Redirect to /login
```

---

## 4. Route Guards

Each app wraps its routes in a guard component that checks:
1. Is a token present in `localStorage`?
2. Is the token valid? (decode JWT, check `exp`)
3. Does the user's role match the required role for this app?

### Route-to-Role Mapping

**Command Center (`/command`)**
```typescript
const COMMAND_ROUTES = [
  { path: '/command',              requiredRole: 'inspector', layout: CommandLayout },
  { path: '/command/dashboard',    requiredRole: 'inspector' },
  { path: '/command/map',          requiredRole: 'inspector' },
  { path: '/command/graph',        requiredRole: 'inspector' },
  { path: '/command/llm',          requiredRole: 'inspector' },
  { path: '/command/cases',        requiredRole: 'inspector' },
  { path: '/command/cases/:id',    requiredRole: 'inspector' },
  { path: '/command/alerts',       requiredRole: 'inspector' },
];
```

**Field Dashboard (`/field`)**
```typescript
const FIELD_ROUTES = [
  { path: '/field',                requiredRole: 'constable', layout: FieldLayout },
  { path: '/field/alerts',         requiredRole: 'constable' },
  { path: '/field/alerts/:id',     requiredRole: 'constable' },
  { path: '/field/dispatch',       requiredRole: 'constable' },
  { path: '/field/history',        requiredRole: 'constable' },
];
```

**Admin Panel (`/admin`)**
```typescript
const ADMIN_ROUTES = [
  { path: '/admin',                requiredRole: 'admin', layout: AdminLayout },
  { path: '/admin/users',          requiredRole: 'admin' },
  { path: '/admin/health',         requiredRole: 'admin' },
  { path: '/admin/audit',          requiredRole: 'admin' },
  { path: '/admin/models',         requiredRole: 'admin' },
  { path: '/admin/complaints',     requiredRole: 'admin' },
  { path: '/admin/evidence',       requiredRole: 'admin' },
];
```

### Guard Behavior
```
if (!token)       → Redirect to /login
if (token expired) → Attempt refresh → if fails, redirect to /login
if (role mismatch) → Redirect to /unauthorized (shows "You don't have access to this page")
```

---

## 5. Role-Based UI Behavior

Not just route-level — UI elements also respect roles:

| Element | Who sees it |
|---------|-------------|
| Admin Panel nav link | `admin` only |
| Command Center nav link | `inspector` + `admin` |
| Field Dashboard nav link | `constable` + `admin` |
| "Trigger Verification" button | `inspector` + `admin` |
| "Request Freeze" button | `inspector` + `admin` |
| "Dispatch Patrol" button | `inspector` + `admin` + `constable` |
| "Backup Request" button | `constable` + `admin` |
| "Generate FIR" button | `inspector` + `admin` |
| User management (CRUD) | `admin` only |
| Audit log | `admin` only |
| System health | `admin` only |
| Model metrics | `admin` only |

---

## 6. Logout

1. Call `POST /api/auth/logout` (invalidates the refresh token server-side).
2. Clear `localStorage` keys: `access`, `refresh`.
3. Disconnect WebSocket.
4. Clear Redux store (dispatch `auth/logout`).
5. Redirect to `/login`.

---

## 7. Session Expiration Handling

### Access Token Expiry
- Frontend checks JWT `exp` claim before attaching to requests.
- If expired, transparently refresh (see §3).
- If refresh also fails, force logout.

### Refresh Token Expiry
- If the refresh call returns 401, the session is dead.
- Show a toast: "Your session has expired. Please log in again."
- Redirect to `/login`.

### Cross-Tab Sync
- Listen for `storage` events on `window` to detect logout from another tab.
- When `localStorage.removeItem('access')` fires in another tab, this tab also logs out.

---

## 8. Security Hygiene Checklist

- [ ] Tokens stored in `localStorage` (demo trade-off — note for judges).
- [ ] All API inputs validated client-side with Zod (same schemas as backend Pydantic).
- [ ] PII masked in API responses (backend responsibility — confirm with M2).
- [ ] No sensitive data in Redux store that persists to disk.
- [ ] Logout clears all auth state.
- [ ] WebSocket connection authenticated on handshake.
- [ ] CORS: frontend origin only.
- [ ] CSP headers set by nginx gateway.
- [ ] Rate limiting enforced by backend (100 req/min/user).
- [ ] No secrets in client-side code (env vars prefixed `VITE_` are public by design).
