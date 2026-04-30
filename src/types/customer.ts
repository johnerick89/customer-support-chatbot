/** Session payload from POST /auth/verify (stored in sessionStorage). */
export type Customer = {
  id: string;
  /** Same as `id`; echoed for APIs that expect `customer_id`. */
  customer_id?: string;
  pin: string;
  email: string;
  name?: string;
  phone?: string;
};
