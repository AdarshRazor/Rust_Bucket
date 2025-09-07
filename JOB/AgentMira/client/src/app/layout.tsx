/**
 * Root Layout Component for Agent Mira Frontend
 * Provides global layout, metadata, and context providers
 * Location: client/src/app/layout.tsx
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Agent Mira - AI Property Recommendations",
  description: "Get personalized property recommendations powered by AI. Find your perfect home with intelligent matching based on your preferences.",
  keywords: ["property", "real estate", "AI", "recommendations", "home buying"],
  authors: [{ name: "Agent Mira Team" }],
  viewport: "width=device-width, initial-scale=1",
  robots: "index, follow",
  openGraph: {
    title: "Agent Mira - AI Property Recommendations",
    description: "Get personalized property recommendations powered by AI",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Agent Mira - AI Property Recommendations",
    description: "Get personalized property recommendations powered by AI",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
          {/* Header */}
          <header className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <h1 className="text-2xl font-bold text-indigo-600">
                      🏠 Agent Mira
                    </h1>
                  </div>
                  <nav className="hidden md:ml-6 md:flex md:space-x-8">
                    <a
                      href="#"
                      className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      Home
                    </a>
                    <a
                      href="#"
                      className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      Properties
                    </a>
                    <a
                      href="#"
                      className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                    >
                      About
                    </a>
                  </nav>
                </div>
                <div className="flex items-center space-x-4">
                  <button className="text-gray-500 hover:text-gray-900">
                    <span className="sr-only">Search</span>
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </button>
                  <button className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700">
                    Get Started
                  </button>
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1">
            {children}
          </main>

          {/* Footer */}
          <footer className="bg-gray-800 text-white">
            <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div className="col-span-1 md:col-span-2">
                  <h3 className="text-lg font-semibold mb-4">Agent Mira</h3>
                  <p className="text-gray-300 mb-4">
                    AI-powered property recommendations to help you find your perfect home.
                    Our intelligent system analyzes your preferences to match you with the best properties.
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 tracking-wider uppercase mb-4">
                    Product
                  </h4>
                  <ul className="space-y-2">
                    <li><a href="#" className="text-gray-300 hover:text-white">Features</a></li>
                    <li><a href="#" className="text-gray-300 hover:text-white">Pricing</a></li>
                    <li><a href="#" className="text-gray-300 hover:text-white">API</a></li>
                  </ul>
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 tracking-wider uppercase mb-4">
                    Support
                  </h4>
                  <ul className="space-y-2">
                    <li><a href="#" className="text-gray-300 hover:text-white">Help Center</a></li>
                    <li><a href="#" className="text-gray-300 hover:text-white">Contact Us</a></li>
                    <li><a href="#" className="text-gray-300 hover:text-white">Privacy Policy</a></li>
                  </ul>
                </div>
              </div>
              <div className="mt-8 pt-8 border-t border-gray-700">
                <p className="text-gray-400 text-sm text-center">
                  © 2024 Agent Mira. All rights reserved.
                </p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}