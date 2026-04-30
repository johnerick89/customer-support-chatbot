/** Session payload from POST /auth/verify (stored in sessionStorage). */
export type Customer = {
  id: string;
  customer_id?: string;
  pin: string;
  email: string;
  name?: string;
  /** From MCP verify result (e.g. admin). */
  role?: string;
  phone?: string;
};
