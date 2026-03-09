import type { PropsWithChildren } from "react";

export function AppLayout({ children }: PropsWithChildren) {
  return (
    <main>
      <h1>NightOwl Control Center</h1>
      <section>{children}</section>
    </main>
  );
}
