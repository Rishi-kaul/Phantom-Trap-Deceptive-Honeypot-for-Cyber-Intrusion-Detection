import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4 text-center text-xl font-bold">
        SSH Honeypot Dashboard
      </header>
      
      <main className="p-6">{children}</main>
      
      <footer className="bg-gray-800 p-4 text-center text-sm">
        &copy; 2025 Phantom Trap | Honeypot for Cyber Intrusion Detection
      </footer>
    </div>
  );
}
