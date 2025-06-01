import type React from "react";
import "@/app/globals.css";
import {  Instrument_Sans } from "next/font/google";
const inter = Instrument_Sans({ subsets: ["latin"] });

export const metadata = {
  title: "Captr - Transform YouTube Videos into Research Documents",
  description:
    "Instantly transform YouTube videos into comprehensive research documents",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
