# Design — Customer Support Chatbot

Technical architecture, data flows, and agent behavior. For assessment context see `task.md`.

## 1. High-level layout (top → bottom)

```text
[ User Browser ]
        │
        ▼
Next.js (Vercel)
├── /login — email + PIN form
└── /chat — streaming chat (protected when gated from `/`)
        │
        │ POST /api/stream (proxied to FastAPI `/stream`)
        │ POST /auth/verify (proxied to FastAPI `/auth/verify`)
        ▼
FastAPI
├── POST /auth/verify — verify customer (prototype may accept any credentials; production calls MCP)
├── POST /stream — agent + streaming response
└── Stateless: no DB, no server sessions, no JWT (prototype)
        │
        ▼
MCP (Streamable HTTP)
└── https://order-mcp-74afyau24q-uc.a.run.app/mcp
```

Local dev: Next rewrites `/auth/verify` and `/api/stream` to `API_ORIGIN` (default `http://127.0.0.1:8000`). See `frontend/next.config.ts`.

## 2. Frontend layer (Next.js)

- **`/`** — session gate: chat if `sessionStorage` has customer, else login.
- **`/login`** — email + PIN → `POST /auth/verify`.
- **`/chat`** — same chat UI; messages → `POST /api/stream` with `customer_id` from stored customer.

### Frontend state

- Customer payload (including `id`, `email`, `name`, …) in **`sessionStorage`** under key `customer`, synced via `useSyncExternalStore` and a small custom event for same-tab updates (`frontend/src/lib/customerSession.ts`).

## 3. Backend layer (FastAPI)

- **`POST /auth/verify`** — body: `{ email, pin }`; returns customer-shaped JSON for the UI (prototype vs production MCP-backed verify is implementation-specific).
- **`POST /stream`** — body includes message + `customer_id`; streams tokens/text back to the client.

### Prototype constraints

- No database.
- No server-side sessions.
- No JWT (credentials / trust model to be hardened before production).

## 4. MCP layer (intended tool surface)

**Product**

- `list_products`
- `search_products`
- `get_product`

**Customer**

- `verify_customer_pin`
- `get_customer`

**Orders**

- `list_orders`
- `get_order`
- `create_order`

## 5. Authentication flow (target)

1. User opens `/login` (or `/` when logged out).
2. Frontend → `POST /auth/verify`.
3. Backend → MCP `verify_customer_pin` (when wired).
4. MCP → backend: customer identifiers + display fields.
5. Backend → frontend: customer JSON.
6. Frontend persists customer in `sessionStorage` and navigates into chat.

## 6. Chat / agent flow (target)

1. User sends a message.
2. Frontend → `POST /stream` with `customer_id` (and message).
3. Backend builds agent context and invokes the LLM.
4. Agent chooses: call an MCP tool or respond directly.
5. MCP runs tools when selected.
6. Response streams to the client (encoding/media type per API contract).
7. Frontend updates the transcript incrementally.

## 7. Agent design

### Intent → tool mapping (illustrative)

| User intent | Tools |
| --- | --- |
| Find products | `search_products` / `list_products` |
| Product details | `get_product` |
| My orders | `list_orders` (scoped with `customer_id`) |
| Order details | `get_order` |
| Buy / place order | `create_order` |

### Agent rules

- Always pass `customer_id` for order-related tool calls.
- Never call `create_order` without explicit user confirmation.
- Prefer `search_products` for vague queries; `get_product` when SKU is known.
- Validate product details before placing an order.
- Prefer MCP-backed facts over unsupported invention.

## 8. Example conversation (illustrative)

**User:** “I need a monitor”

→ Agent calls `search_products(query="monitor")` → MCP returns candidates → agent summarizes options.

**User:** “I want the Dell 27-inch one”

→ Agent calls `get_product(sku="MON-XXXX")` → confirms details with the user.

**User:** “Buy 2”

→ Agent asks for confirmation → on confirm, calls `create_order(...)`.
