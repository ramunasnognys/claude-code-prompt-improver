import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SaaS App",
  description: "Next.js SaaS application with Supabase",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
