import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
// import { ClerkProvider } from '@clerk/nextjs';

import './globals.css';
import { Providers } from './providers';
import { Navbar } from '@/components/navbar';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export const metadata: Metadata = {
  title: 'Implodesc - AI Supply Chain Analysis',
  description: 'Comprehensive AI-driven supply chain analysis with carbon footprint calculations',
  keywords: ['supply chain', 'AI', 'carbon footprint', 'sustainability', 'analysis'],
  authors: [{ name: 'Implodesc Team' }],
  creator: 'Implodesc',
  publisher: 'Implodesc',
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://implodesc.com',
    title: 'Implodesc - AI Supply Chain Analysis',
    description: 'Comprehensive AI-driven supply chain analysis with carbon footprint calculations',
    siteName: 'Implodesc',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Implodesc - AI Supply Chain Analysis',
    description: 'Comprehensive AI-driven supply chain analysis with carbon footprint calculations',
    creator: '@implodesc',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className={inter.variable}>
          <Providers>
            <div className="relative flex min-h-screen flex-col">
              <Navbar />
              <div className="flex-1">{children}</div>
            </div>
          </Providers>
        </body>
      </html>
    // </ClerkProvider>
  );
}