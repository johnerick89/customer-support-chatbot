"use client";

import {
  getCustomerJsonSnapshot,
  getServerCustomerJsonSnapshot,
  subscribeCustomerJson,
} from "@/lib/customerSession";
import { useSyncExternalStore } from "react";
import Chat from "./chat/page";
import Login from "./login/page";

export default function Home() {
  const customerJson = useSyncExternalStore(
    subscribeCustomerJson,
    getCustomerJsonSnapshot,
    getServerCustomerJsonSnapshot,
  );

  if (customerJson) {
    return <Chat />;
  }

  return <Login />;
}
