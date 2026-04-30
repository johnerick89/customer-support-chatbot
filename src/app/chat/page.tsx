"use client";

import {
  CUSTOMER_STORAGE_KEY,
  getCustomerJsonSnapshot,
  getServerCustomerJsonSnapshot,
  notifyCustomerSessionChanged,
  subscribeCustomerJson,
} from "@/lib/customerSession";
import { Customer } from "@/types/customer";
import { useRouter } from "next/navigation";
import { useMemo, useState, useSyncExternalStore } from "react";
import { toast } from "react-hot-toast";

function initials(name: string | undefined, email: string) {
  const n = name?.trim();
  if (n) {
    const parts = n.split(/\s+/).filter(Boolean);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return n.slice(0, 2).toUpperCase();
  }
  const local = email.split("@")[0]?.trim() || "?";
  return local.slice(0, 2).toUpperCase();
}

export default function Chat() {
  const router = useRouter();
  const customerJson = useSyncExternalStore(
    subscribeCustomerJson,
    getCustomerJsonSnapshot,
    getServerCustomerJsonSnapshot,
  );

  const customer = useMemo((): Customer | null => {
    if (!customerJson) return null;
    try {
      return JSON.parse(customerJson) as Customer;
    } catch {
      return null;
    }
  }, [customerJson]);

  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);

  const signOut = () => {
    sessionStorage.removeItem(CUSTOMER_STORAGE_KEY);
    notifyCustomerSessionChanged();
    router.push("/");
  };

  const send = async () => {
    const trimmed = input.trim();
    if (!trimmed || sending) return;

    const customerId = customer?.id ?? customer?.customer_id;
    if (!customerId?.trim()) {
      toast.error("Missing customer id — sign in again.");
      return;
    }

    setSending(true);
    const res = await fetch("/api/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: trimmed,
        customer_id: customerId.trim(),
        customer_name: customer?.name ?? null,
        customer_email: customer?.email ?? null,
      }),
    });

    if (!res.ok) {
      toast.error("Failed to send message");
      setSending(false);
      return;
    }

    setInput("");

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();
    let text = "";

    setMessages((prev) => [...prev, ""]);

    try {
      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        text += decoder.decode(value);
        setMessages((prev) => [...prev.slice(0, -1), text]);
      }
    } finally {
      setSending(false);
    }
  };

  const displayName = customer?.name?.trim() || customer?.email || "there";
  const avatar = initials(customer?.name, customer?.email ?? "");

  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 font-sans text-zinc-900 dark:bg-zinc-950 dark:text-zinc-50">
      <header className="sticky top-0 z-10 border-b border-zinc-200/80 bg-white/85 px-4 py-4 backdrop-blur-md dark:border-zinc-800 dark:bg-zinc-950/85">
        <div className="mx-auto flex max-w-2xl items-center justify-between gap-4">
          <div className="flex min-w-0 items-center gap-3">
            <div
              className="flex size-11 shrink-0 items-center justify-center rounded-2xl bg-linear-to-br from-violet-500 to-fuchsia-600 text-sm font-bold text-white shadow-lg shadow-violet-500/25"
              aria-hidden
            >
              {avatar}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium uppercase tracking-wider text-violet-600 dark:text-violet-400">
                Meridian support
              </p>
              <h1 className="truncate text-lg font-semibold tracking-tight">
                Hi, {displayName}
              </h1>
            </div>
          </div>
          <button
            type="button"
            onClick={signOut}
            className="shrink-0 rounded-xl border border-zinc-200 px-3 py-2 text-xs font-medium text-zinc-600 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col px-4 py-6">
        <div className="flex flex-1 flex-col overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-xl shadow-zinc-900/5 dark:border-zinc-800 dark:bg-zinc-900/60 dark:shadow-black/30">
          <div className="min-h-[min(60vh,28rem)] flex-1 space-y-4 overflow-y-auto p-4 sm:p-5">
            {messages.length === 0 ? (
              <div className="flex h-full min-h-48 flex-col items-center justify-center rounded-xl border border-dashed border-zinc-200 bg-zinc-50/80 px-6 py-12 text-center dark:border-zinc-700 dark:bg-zinc-950/40">
                <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                  Start a conversation
                </p>
                <p className="mt-1 max-w-xs text-xs text-zinc-500 dark:text-zinc-500">
                  Ask anything about your account or orders. Replies stream in as
                  they arrive.
                </p>
              </div>
            ) : (
              messages.map((m, i) => (
                <div key={i} className="flex justify-start">
                  <div className="max-w-[92%] rounded-2xl rounded-tl-md border border-zinc-100 bg-zinc-50 px-4 py-3 text-sm leading-relaxed text-zinc-800 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/80 dark:text-zinc-100">
                    <p className="whitespace-pre-wrap wrap-break-word">{m}</p>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="border-t border-zinc-200 bg-zinc-50/90 p-3 dark:border-zinc-800 dark:bg-zinc-950/80 sm:p-4">
            <div className="flex gap-2 sm:gap-3">
              <input
                className="min-w-0 flex-1 rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm outline-none transition placeholder:text-zinc-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 disabled:opacity-60 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:border-violet-400 dark:focus:ring-violet-400/20"
                placeholder="Type your message…"
                value={input}
                disabled={sending}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    void send();
                  }
                }}
              />
              <button
                type="button"
                onClick={() => void send()}
                disabled={sending || !input.trim()}
                className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-zinc-900 px-5 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-zinc-800 disabled:pointer-events-none disabled:opacity-40 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-100"
              >
                {sending ? (
                  <span
                    className="size-4 animate-spin rounded-full border-2 border-white/30 border-t-white dark:border-zinc-900/30 dark:border-t-zinc-900"
                    aria-hidden
                  />
                ) : null}
                Send
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
