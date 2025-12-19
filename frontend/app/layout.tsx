import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "⚡ DevJobs Hunter - Moteur d'Emploi IT",
  description: "Moteur de recherche d'emploi cyberpunk pour devs · Multi-sources · Scraping · Design néon",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}

