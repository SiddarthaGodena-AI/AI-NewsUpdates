import "./globals.css";

export const metadata = {
  title: "SmartNews AI",
  description: "Premium AI news summarizer",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
