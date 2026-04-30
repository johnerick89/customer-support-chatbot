import type { NextConfig } from "next";

/**
 * - Local: proxy to uvicorn on API_ORIGIN (default http://127.0.0.1:8000).
 * - Vercel (no API_ORIGIN): proxy to the Python serverless entry `api/index.py`.
 * - Vercel + API_ORIGIN: proxy to an external FastAPI host (e.g. separate service).
 */
function apiRewrites() {
  const explicit = process.env.API_ORIGIN?.trim();
  if (explicit) {
    const base = explicit.replace(/\/$/, "");
    return [
      { source: "/auth/verify", destination: `${base}/auth/verify` },
      { source: "/auth/verify/", destination: `${base}/auth/verify` },
      { source: "/api/stream", destination: `${base}/stream` },
      { source: "/api/stream/", destination: `${base}/stream` },
    ];
  }

  if (process.env.VERCEL === "1") {
    return [
      { source: "/auth/verify", destination: "/api/index" },
      { source: "/auth/verify/", destination: "/api/index" },
      { source: "/api/stream", destination: "/api/index" },
      { source: "/api/stream/", destination: "/api/index" },
    ];
  }

  const local = "http://127.0.0.1:8000";
  return [
    { source: "/auth/verify", destination: `${local}/auth/verify` },
    { source: "/auth/verify/", destination: `${local}/auth/verify` },
    { source: "/api/stream", destination: `${local}/stream` },
    { source: "/api/stream/", destination: `${local}/stream` },
  ];
}

const nextConfig: NextConfig = {
  output: "standalone",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return apiRewrites();
  },
};

export default nextConfig;
