import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NPCWoods Telemedicine — $59 Text-Based Care with Chris Woods, NP",
  description: "$59 text-based telemedicine with Chris Woods, NP, available in 11 states.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
    apple: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
