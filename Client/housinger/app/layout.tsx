import { montserrat } from '../components/ui/fonts';
import '../components/ui/global.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${montserrat.className} antialiased`}>
        {children}
        <footer className='flex justify-center items-center py-10'>
          Footer Here!
        </footer>
      </body>
    </html>
  );
}
