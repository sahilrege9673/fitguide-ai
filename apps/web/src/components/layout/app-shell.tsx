'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';
import { 
  LayoutDashboard, 
  Dumbbell, 
  Calendar, 
  BookOpen, 
  MessageSquare, 
  TrendingUp, 
  User, 
  LogOut,
  ChevronRight,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface AppShellProps {
  children: React.ReactNode;
}

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Workouts', href: '/workouts', icon: Dumbbell },
  { name: 'Schedule', href: '/schedule', icon: Calendar },
  { name: 'Exercise Library', href: '/exercises', icon: BookOpen },
  { name: 'AI Assistant', href: '/assistant', icon: MessageSquare },
  { name: 'Progress', href: '/progress', icon: TrendingUp },
  { name: 'Profile', href: '/profile', icon: User },
];

export function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const handleSignOut = async () => {
    try {
      const supabase = createClient();
      await supabase.auth.signOut();
      router.push('/login');
      router.refresh();
    } catch (err) {
      console.error('Sign out error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-carbon text-chalk flex flex-col lg:flex-row selection:bg-lime selection:text-carbon">
      
      {/* DESKTOP FIXED LEFT RAIL (>= 1024px) */}
      <aside className="hidden lg:flex w-64 flex-col justify-between border-r border-forest bg-carbon fixed inset-y-0 z-50">
        <div className="flex flex-col">
          {/* Brand Header */}
          <div className="h-16 flex items-center gap-2.5 px-6 border-b border-forest">
            <span className="h-2.5 w-2.5 bg-lime rounded-none" />
            <Link href="/dashboard" className="font-display text-lg font-bold tracking-tight text-chalk">
              FEEDGUIDE<span className="text-lime">.AI</span>
            </Link>
            <span className="text-[10px] font-mono uppercase tracking-widest text-sand border border-forest px-1 py-0.2 ml-auto">
              CORE
            </span>
          </div>

          {/* Navigation Items */}
          <nav className="p-4 space-y-1">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-sm text-xs font-mono uppercase tracking-wider transition-colors duration-fast ${
                    isActive
                      ? 'bg-forest text-lime border-l-2 border-lime font-semibold'
                      : 'text-sand hover:text-chalk hover:bg-forest/30'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`h-4 w-4 ${isActive ? 'text-lime' : 'text-sand'}`} />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] font-mono text-sand/60 border border-forest/60 px-1 py-0.5 rounded-none">
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Footer Athlete Utility */}
        <div className="p-4 border-t border-forest space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-sand">
            <span>INVARIANTS</span>
            <span className="text-lime flex items-center gap-1 font-semibold">
              <span className="h-1.5 w-1.5 rounded-full bg-lime" /> ACTIVE
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleSignOut}
            className="w-full justify-start text-xs font-mono text-sand hover:text-burnt"
          >
            <LogOut className="h-4 w-4 mr-2" /> Sign Out
          </Button>
        </div>
      </aside>

      {/* MOBILE TOP BAR (< 1024px) */}
      <div className="lg:hidden flex items-center justify-between h-14 px-4 border-b border-forest bg-carbon sticky top-0 z-50">
        <Link href="/dashboard" className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 bg-lime" />
          <span className="font-display text-base font-bold tracking-tight text-chalk">
            FEEDGUIDE<span className="text-lime">.AI</span>
          </span>
        </Link>
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="p-2 text-sand hover:text-chalk"
          aria-label="Toggle navigation menu"
        >
          {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* MOBILE DRAWER OVERLAY */}
      {isMobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-40 bg-carbon/95 p-6 pt-20 space-y-4">
          <div className="space-y-2">
            {NAV_ITEMS.map((item) => {
              const isActive = pathname.startsWith(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={`flex items-center justify-between p-3 rounded-sm text-sm font-mono uppercase tracking-wider ${
                    isActive ? 'bg-forest text-lime' : 'text-sand'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && <span className="text-xs text-sand/60">{item.badge}</span>}
                </Link>
              );
            })}
          </div>
          <div className="border-t border-forest pt-4">
            <Button variant="danger" size="sm" onClick={handleSignOut} className="w-full">
              Sign Out
            </Button>
          </div>
        </div>
      )}

      {/* MOBILE BOTTOM TAB BAR */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 h-16 border-t border-forest bg-carbon/95 backdrop-blur-md z-40 flex items-center justify-around px-2 pb-safe">
        {[
          { name: 'Hub', href: '/dashboard', icon: LayoutDashboard },
          { name: 'Workouts', href: '/workouts', icon: Dumbbell },
          { name: 'Schedule', href: '/schedule', icon: Calendar },
          { name: 'Exercises', href: '/exercises', icon: BookOpen },
          { name: 'Profile', href: '/profile', icon: User },
        ].map((item) => {
          const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center min-w-[56px] h-full ${
                isActive ? 'text-lime' : 'text-sand'
              }`}
            >
              <Icon className="h-5 w-5 mb-0.5" />
              <span className="text-[10px] font-mono uppercase tracking-wider">{item.name}</span>
            </Link>
          );
        })}
      </div>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 lg:pl-64 min-h-screen pb-20 lg:pb-8">
        {children}
      </main>

    </div>
  );
}
