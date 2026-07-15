import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host =
    requestHeaders.get("x-forwarded-host") ??
    requestHeaders.get("host") ??
    "localhost:3000";
  const protocol =
    requestHeaders.get("x-forwarded-proto") ??
    (host.startsWith("localhost") || host.startsWith("127.0.0.1")
      ? "http"
      : "https");
  const metadataBase = new URL(`${protocol}://${host}`);
  const socialImage = new URL("/og.png", metadataBase).toString();
  const title = "NPCWoods Telemedicine — $59 Text-Based Care with Chris Woods, NP";
  const description =
    "$59 flat fee for text-based telemedicine with Chris Woods, NP, available in 11 states.";
  const socialTitle = "Feeling rough? Just text me.";

  return {
    metadataBase: metadataBase,
    title,
    description,
    icons: {
      icon: "/favicon.svg",
      shortcut: "/favicon.svg",
      apple: "/favicon.svg",
    },
    openGraph: {
      title: socialTitle,
      description,
      url: metadataBase,
      images: [
        {
          url: socialImage,
          width: 1200,
          height: 630,
          alt: "Feeling rough? Just text me. $59 flat fee.",
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: socialTitle,
      description,
      images: [
        {
          url: socialImage,
          width: 1200,
          height: 630,
          alt: "Feeling rough? Just text me. $59 flat fee.",
        },
      ],
    },
  };
}

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
