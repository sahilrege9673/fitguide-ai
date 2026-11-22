import Link from 'next/link';
import { Button } from '@/components/ui/button';

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-forest bg-carbon/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2 group">
          <span className="h-3 w-3 bg-lime rounded-none" />
          <span className="font-display text-xl font-bold tracking-tighter text-chalk group-hover:text-lime transition-colors duration-fast">
            FITGUIDE<span className="text-lime">.AI</span>
          </span>
          <span className="hidden sm:inline-block text-[10px] uppercase font-mono tracking-widest text-sand border border-forest px-1.5 py-0.5 ml-1">
            LAB V1.0
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-8 text-xs uppercase tracking-widest text-sand font-mono">
          <Link href="#methodology" className="hover:text-chalk transition-colors duration-fast">
            Methodology
          </Link>
          <Link href="#safety" className="hover:text-chalk transition-colors duration-fast">
            Safety Invariants
          </Link>
          <Link href="#catalog" className="hover:text-chalk transition-colors duration-fast">
            Exercise Catalog
          </Link>
        </nav>

        <div className="flex items-center gap-3">
          <Link href="/login">
            <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
              Sign In
            </Button>
          </Link>
          <Link href="/register">
            <Button variant="primary" size="sm">
              Start Assessment
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
