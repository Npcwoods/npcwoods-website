import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

const safeMetadataBase = new URL("http://localhost:3000");

function firstHeaderValue(value: string | null): string | null {
  const firstValue = value?.split(",", 1)[0]?.trim();
  return firstValue || null;
}

function isValidHost(host: string): boolean {
  if (host.length > 253 || /[\s\\/@?#]/.test(host)) return false;

  const bracketedIpv6 = host.match(/^\[[0-9a-f:.]+\](?::(\d{1,5}))?$/i);
  if (bracketedIpv6) {
    return bracketedIpv6[1] === undefined || Number(bracketedIpv6[1]) <= 65535;
  }

  const hostnameAndPort = host.match(/^([a-z0-9.-]+)(?::(\d{1,5}))?$/i);
  if (!hostnameAndPort) return false;
  if (hostnameAndPort[2] !== undefined && Number(hostnameAndPort[2]) > 65535) {
    return false;
  }

  return hostnameAndPort[1].split(".").every(
    (label) =>
      label.length > 0 &&
      label.length <= 63 &&
      /^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i.test(label),
  );
}

function isNumericIpv4Loopback(hostname: string): boolean {
  const octets = hostname.split(".");
  return (
    octets.length === 4 &&
    octets.every(
      (octet) => /^\d{1,3}$/.test(octet) && Number(octet) <= 255,
    ) &&
    Number(octets[0]) === 127
  );
}

function resolveMetadataBase(host: string, forwardedProtocol: string | null): URL {
  try {
    if (!isValidHost(host)) return safeMetadataBase;

    const parsedHost = new URL(`http://${host}`);
    const hostname = parsedHost.hostname.toLowerCase();
    const isLocalhost =
      hostname === "localhost" ||
      hostname.endsWith(".localhost") ||
      isNumericIpv4Loopback(hostname) ||
      hostname === "[::1]" ||
      hostname === "::1";
    const normalizedProtocol = forwardedProtocol?.toLowerCase();
    const protocol =
      normalizedProtocol === "http" || normalizedProtocol === "https"
        ? normalizedProtocol
        : isLocalhost
          ? "http"
          : "https";

    return new URL(`${protocol}://${host}`);
  } catch {
    return safeMetadataBase;
  }
}

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host =
    firstHeaderValue(requestHeaders.get("x-forwarded-host")) ??
    firstHeaderValue(requestHeaders.get("host")) ??
    "localhost:3000";
  const forwardedProtocol = firstHeaderValue(
    requestHeaders.get("x-forwarded-proto"),
  );
  const metadataBase = resolveMetadataBase(host, forwardedProtocol);
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
