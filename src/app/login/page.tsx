"use client";

import { notifyCustomerSessionChanged } from "@/lib/customerSession";
import { useRouter } from "next/navigation";
import { useState } from "react";

function apiErrorMessage(data: Record<string, unknown>): string | null {
  if (typeof data.message === "string") return data.message;
  if (typeof data.detail === "string") return data.detail;
  return null;
}

const highlights = [
  {
    title: "Product & availability",
    body: "Ask about monitors, keyboards, printers, networking gear, and accessories — and what is in stock.",
  },
  {
    title: "Orders & history",
    body: "Get help placing orders and looking up what you have ordered before, without waiting on email.",
  },
  {
    title: "Signed-in support",
    body: "Returning customers sign in with email and PIN so answers can be tied to your account safely.",
  },
];

export default function Login() {
  const [email, setEmail] = useState("");
  const [pin, setPin] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const login = async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch("/auth/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, pin }),
      });

      const data = (await res.json().catch(() => ({}))) as Record<
        string,
        unknown
      >;

      if (!res.ok) {
        setError(
          apiErrorMessage(data) ??
            "We could not verify those details. Try again.",
        );
        return;
      }

      sessionStorage.setItem("customer", JSON.stringify(data));
      notifyCustomerSessionChanged();
      router.push("/");
    } catch {
      setError("Something went wrong. Check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  const canSubmit = email.trim().length > 0 && pin.length > 0 && !loading;

  return (
    <div className="min-h-screen bg-zinc-50 font-sans text-zinc-900 dark:bg-zinc-950 dark:text-zinc-50">
      <div className="grid min-h-screen lg:grid-cols-2">
        {/* Welcome / story — left on large screens */}
        <div className="relative flex flex-col justify-between overflow-hidden bg-zinc-900 px-8 py-12 text-zinc-100 sm:px-12 lg:px-14 lg:py-16">
          <div
            className="pointer-events-none absolute inset-0 opacity-50"
            aria-hidden
          >
            <div className="absolute -right-20 top-0 size-112 rounded-full bg-violet-600/35 blur-3xl" />
            <div className="absolute -left-32 bottom-0 h-72 w-72 rounded-full bg-cyan-500/20 blur-3xl" />
            <div className="absolute left-1/3 top-1/2 h-64 w-64 -translate-y-1/2 rounded-full bg-fuchsia-500/15 blur-3xl" />
          </div>

          <div className="relative">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-violet-300">
              Meridian Electronics
            </p>
            <h1 className="mt-4 max-w-xl text-3xl font-semibold leading-tight tracking-tight sm:text-4xl lg:text-[2.35rem] lg:leading-[1.15]">
              Customer support, reimagined with AI
            </h1>
            <p className="mt-5 max-w-md text-sm leading-relaxed text-zinc-400">
              Meridian sells computer products across monitors, keyboards,
              printers, networking, and accessories. This prototype lets you
              chat with an assistant that can call into our internal order
              systems — so common questions do not have to start on the phone.
            </p>
          </div>

          <ul className="relative mt-12 space-y-6 lg:mt-0">
            {highlights.map((item) => (
              <li key={item.title} className="flex gap-4">
                <span
                  className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-white/10 text-violet-200 ring-1 ring-white/10"
                  aria-hidden
                >
                  <svg
                    className="size-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </span>
                <div>
                  <p className="font-medium text-white">{item.title}</p>
                  <p className="mt-1 text-sm leading-relaxed text-zinc-400">
                    {item.body}
                  </p>
                </div>
              </li>
            ))}
          </ul>

          <p className="relative mt-12 text-xs leading-relaxed text-zinc-500 lg:mt-8">
            Built for leadership and CX review: a working path from sign-in to
            chat, with room to harden security and cost controls before wider
            rollout.
          </p>
        </div>

        {/* Sign-in — right on large screens */}
        <div className="relative flex flex-col justify-center px-4 py-12 sm:px-8 lg:px-12 lg:py-16">
          <div
            className="pointer-events-none absolute inset-0 opacity-30 dark:opacity-20 lg:hidden"
            aria-hidden
          >
            <div className="absolute right-0 top-24 h-64 w-64 rounded-full bg-violet-400/25 blur-3xl" />
          </div>

          <div className="relative mx-auto w-full max-w-md">
            <div className="mb-8 lg:hidden">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-violet-600 dark:text-violet-400">
                Meridian
              </p>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight">
                Sign in
              </h2>
              <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                Use your Meridian email and PIN to open the support chat.
              </p>
            </div>

            <div className="hidden lg:block lg:mb-8">
              <h2 className="text-2xl font-semibold tracking-tight">
                Sign in
              </h2>
              <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                Enter your Meridian email and PIN. Your session stays in this
                browser only.
              </p>
            </div>

            <div className="rounded-2xl border border-zinc-200/80 bg-white/95 p-8 shadow-xl shadow-zinc-900/5 backdrop-blur-sm dark:border-zinc-800 dark:bg-zinc-900/90 dark:shadow-black/40">
              {error ? (
                <div
                  role="alert"
                  className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800 dark:border-red-900/50 dark:bg-red-950/40 dark:text-red-200"
                >
                  {error}
                </div>
              ) : null}

              <form
                className="space-y-5"
                onSubmit={(e) => {
                  e.preventDefault();
                  if (canSubmit) void login();
                }}
              >
                <div className="space-y-2">
                  <label
                    htmlFor="login-email"
                    className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                  >
                    Email
                  </label>
                  <input
                    id="login-email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm outline-none transition placeholder:text-zinc-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:border-violet-400 dark:focus:ring-violet-400/20"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="login-pin"
                    className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                  >
                    PIN
                  </label>
                  <input
                    id="login-pin"
                    name="pin"
                    type="password"
                    autoComplete="current-password"
                    placeholder="••••••"
                    value={pin}
                    onChange={(e) => setPin(e.target.value)}
                    className="w-full rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm outline-none transition placeholder:text-zinc-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:border-violet-400 dark:focus:ring-violet-400/20"
                  />
                </div>

                <button
                  type="submit"
                  disabled={!canSubmit}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-zinc-900 px-4 py-3.5 text-sm font-semibold text-white shadow-lg shadow-zinc-900/25 transition hover:bg-zinc-800 disabled:pointer-events-none disabled:opacity-40 dark:bg-white dark:text-zinc-900 dark:shadow-white/10 dark:hover:bg-zinc-100"
                >
                  {loading ? (
                    <>
                      <span
                        className="size-4 animate-spin rounded-full border-2 border-white/30 border-t-white dark:border-zinc-900/30 dark:border-t-zinc-900"
                        aria-hidden
                      />
                      Signing in…
                    </>
                  ) : (
                    "Continue to chat"
                  )}
                </button>
              </form>
            </div>

            <p className="mt-8 text-center text-xs text-zinc-500 dark:text-zinc-500">
              Protected session · credentials are verified server-side
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
