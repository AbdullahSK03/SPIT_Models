import "./globals.css";

import Navbar from "@/components/Navigation/Navbar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-purple-200">
        <Navbar />
        {children}
      </body>
    </html>
  );
}
