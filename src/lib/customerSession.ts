export const CUSTOMER_STORAGE_KEY = "customer";

const SESSION_EVENT = "meridian-customer-session";

export function notifyCustomerSessionChanged() {
  window.dispatchEvent(new CustomEvent(SESSION_EVENT));
}

export function subscribeCustomerJson(onStoreChange: () => void) {
  const handler = () => onStoreChange();
  window.addEventListener("storage", handler);
  window.addEventListener(SESSION_EVENT, handler);
  return () => {
    window.removeEventListener("storage", handler);
    window.removeEventListener(SESSION_EVENT, handler);
  };
}

export function getCustomerJsonSnapshot(): string | null {
  return sessionStorage.getItem(CUSTOMER_STORAGE_KEY);
}

export function getServerCustomerJsonSnapshot(): null {
  return null;
}
