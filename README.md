# Customer Support Chatbot

## Architecture

### 1. High-Level Layout (Top → Bottom Flow)

[ User Browser ]
│
▼
Next.js (Vercel)
├── /login page — email + PIN form
└── /chat page — SSE chat interface (protected)
│
│ POST /stream (SSE)
│ POST /auth/verify
▼
FastAPI (Vercel)
├── POST /auth/verify → calls verify_customer_pin via MCP
├── POST /stream → runs agent with customer_id in context
└── no database — customer_id held in frontend state only
│
▼
MCPServerStreamableHttp
└── https://order-mcp-74afyau24q-uc.a.run.app/mcp

### 2. Frontend Layer (Next.js)

[ Next.js (Vercel) ]
├── /login page
│ - email + PIN form
│ - calls /auth/verify
│
└── /chat page (protected) - shows customer_name - chat interface - sends messages to /stream - renders SSE responses - logout (clears state)

#### Frontend State

- customer_id
- customer_name
  (storage: React state or sessionStorage)

### 3.Backend Layer (FastAPI)

[ FastAPI Backend ]
├── POST /auth/verify
│ - receives email + PIN
│ - calls MCP: verify_customer_pin
│ - returns customer_id + name
│
└── POST /stream (SSE) - receives message + customer_id - injects into agent context - runs LLM agent - streams response back

- Backend to be Stateless for now :
- No DB
- No sessions
- No JWT (prototype only)

### 4. MCP Layer

[ MCP Server ]
├── Product Tools
│ - list_products
│ - search_products
│ - get_product
│
├── Customer Tools
│ - verify_customer_pin
│ - get_customer
│
└── Order Tools
| - list_orders
| - get_order
| - create_order

### 5. Authentication Flow

1. User → /login (email + PIN)
2. Frontend → POST /auth/verify
3. Backend → MCP: verify_customer_pin
4. MCP → Backend: customer_id, name
5. Backend → Frontend: customer context
6. Frontend stores state

### 6. Chat / Agent Flow

1. User sends message
2. Frontend → POST /stream (with customer_id)
3. Backend:
   - builds agent context
   - calls LLM
4. Agent decides:
   → call MCP tool OR respond directly
5. MCP executes tool (if needed)
6. Response streamed back (SSE)
7. Frontend renders in real-time

### 7. Agent Design

[ LLM Agent ]

Intent → Tool Mapping:

- “Find products” → search_products / list_products
- “View product details” → get_product
- “My orders” → list_orders (with customer_id)
- “Order details” → get_order
- “Buy / place order” → create_order

Agent Rules:

- Always include customer_id for order-related queries
- Never call create_order without explicit user confirmation
- Use search_products for vague queries, get_product for exact SKU
- Validate product details before placing an order
- Prefer MCP tools over generating answers

#### 8. Realistic Chat flow

User: “I need a monitor”

→ Agent:
calls search_products(query="monitor")

→ MCP returns products

→ Agent summarizes options

User: “I want the Dell 27-inch one”

→ Agent:
calls get_product(sku="MON-XXXX")

→ Confirms details

User: “Buy 2”

→ Agent:
asks for confirmation

→ On confirm:
calls create_order(...)
