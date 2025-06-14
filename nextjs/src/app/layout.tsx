// app/layout.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Providers } from "./providers";
import theme from "./theme";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PhishGuard | Real-Time Phishing Protection for Chrome",
  description:
    "Free Chrome extension that detects and blocks phishing sites instantly. Trusted by 10,000+ users.",
  keywords: [
    "phishing protection",
    "chrome extension",
    "cybersecurity",
    "block malicious sites",
  ],
  openGraph: {
    images: ["https://phishguard.vercel.app/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
