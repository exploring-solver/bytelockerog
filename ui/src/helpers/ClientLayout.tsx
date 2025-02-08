'use client';

import { usePathname } from 'next/navigation';
import Navbar from "@/components/Nav";
import Footer from "@/components/Foot";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Conditions to hide the default Navbar and Footer
  const hideNav = ['/sign-in', '/sign-up'].includes(pathname);
  const hideFoot = ['/sign-in', '/sign-up',"/roadmap"].includes(pathname);

  return (
    <>
      {/* Show SpecialNavbar on /main, otherwise show the default Navbar */}
      {!hideNav && <Navbar />}
      {children}
      {!hideFoot && <Footer />}
    </>
  );
}