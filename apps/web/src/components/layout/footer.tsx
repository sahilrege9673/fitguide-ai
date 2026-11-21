import Link from 'next/link';

export function Footer() {
  return (
    <footer className="w-full border-t border-forest bg-carbon-surface mt-20">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 bg-lime" />
              <span className="font-display text-lg font-bold tracking-tight text-chalk">
                FEEDGUIDE<span className="text-lime">.AI</span>
              </span>
            </div>
            <p className="text-sm text-sand/80 max-w-md leading-relaxed">
              Engineered digital fitness companion and workout management platform. 
              Real physical data isolation, age-calibrated programming, and clinical safety invariants.
            </p>
          </div>

          <div>
            <h4 className="text-xs font-mono uppercase tracking-widest text-chalk mb-4">Architecture</h4>
            <ul className="space-y-2 text-xs text-sand font-mono">
              <li>Next.js 14 App Router</li>
              <li>Python FastAPI</li>
              <li>Supabase pgvector</li>
              <li>LoRA Intent Routing</li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-mono uppercase tracking-widest text-chalk mb-4">Integrity</h4>
            <ul className="space-y-2 text-xs text-sand font-mono">
              <li><Link href="#safety" className="hover:text-chalk">Clinical Invariants</Link></li>
              <li><Link href="#credits" className="hover:text-chalk">Attribution Ledger</Link></li>
              <li><span className="text-lime">WCAG AA Compliant</span></li>
              <li><span>Zero Stock 3D Art</span></li>
            </ul>
          </div>
        </div>

        {/* Visible Fitness Disclaimer */}
        <div className="border-t border-forest/60 pt-6 pb-6 text-xs text-sand/70 leading-relaxed">
          <p className="mb-2 font-mono uppercase tracking-wider text-sand">
            [ CLINICAL & FITNESS DISCLAIMER ]
          </p>
          <p>
            FeedGuide AI provides evidence-based exercise guidance and activity tracking for general wellness. It is not a substitute for clinical medical advice, diagnosis, or personalized physical therapy. Always consult a qualified healthcare provider prior to starting any new training regimen, especially if you have pre-existing conditions, injuries, or cardiovascular symptoms.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between border-t border-forest/40 pt-6 text-xs text-sand/60 font-mono">
          <p>&copy; {new Date().getFullYear()} FeedGuide AI. All rights reserved.</p>
          <p className="mt-2 sm:mt-0">Urban Performance / Premium Athletic Identity</p>
        </div>
      </div>
    </footer>
  );
}
