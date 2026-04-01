import { Geist, Geist_Mono, Manrope } from "next/font/google";
import "./globals.css";
import ClientWrapper from "@/components/ClientWrapper";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const manrope = Manrope({
  variable: '--font-manrope',
  subsets: ['latin'],
});


export const metadata = {
  title: "Bitlify",
  description: "The ultimate URL shortener for creators and businesses. Create branded links, track real-time analytics, and optimize your digital presence with ease.",
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${manrope.variable} h-full antialiased dark`}
    >
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&amp;display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet" />
      </head>
      <body className="bg-background-light dark:bg-background-dark font-display font-monr text-slate-900 dark:text-slate-100 antialiased selection:bg-primary/30 ">
        {children}
      </body>
    </html>
  );
}
