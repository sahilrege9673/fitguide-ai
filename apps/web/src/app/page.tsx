import Link from 'next/link';
import { Navbar } from '@/components/layout/navbar';
import { Footer } from '@/components/layout/footer';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ShieldCheck, Target, Activity, Database, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col bg-carbon selection:bg-lime selection:text-carbon">
      <Navbar />

      <main className="flex-1">
        {/* HERO SECTION */}
        <section className="relative overflow-hidden pt-20 pb-24 md:pt-32 md:pb-36 border-b border-forest">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              
              <div className="lg:col-span-7 space-y-6">
                <div className="flex items-center gap-2">
                  <Badge variant="lime">ATHLETIC TECH</Badge>
                  <span className="text-xs font-mono text-sand uppercase tracking-widest">
                    LAB PHASE 1 // GROUNDED ARCHITECTURE
                  </span>
                </div>

                <h1 className="font-display text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-chalk uppercase leading-[1.05]">
                  PRECISION <br />
                  <span className="text-lime">PERFORMANCE.</span> <br />
                  ZERO NOISE.
                </h1>

                <p className="text-base sm:text-lg text-sand leading-relaxed max-w-2xl">
                  Not a generic chatbot or template generator. FeedGuide AI is an engineered digital fitness companion that sequences your training around your verified physiology, equipment constraints, and real logged recovery.
                </p>

                <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-4">
                  <Link href="/register">
                    <Button variant="primary" size="lg" className="w-full sm:w-auto">
                      Start Assessment <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                  <Link href="/login">
                    <Button variant="outline" size="lg" className="w-full sm:w-auto">
                      Athlete Sign In
                    </Button>
                  </Link>
                </div>

                <div className="pt-6 grid grid-cols-3 gap-6 border-t border-forest/60">
                  <div>
                    <div className="font-display text-2xl sm:text-3xl font-bold text-lime tabular-nums">100%</div>
                    <div className="text-[11px] font-mono uppercase tracking-widest text-sand mt-0.5">RLS User Isolated</div>
                  </div>
                  <div>
                    <div className="font-display text-2xl sm:text-3xl font-bold text-chalk tabular-nums">&gt;= 80</div>
                    <div className="text-[11px] font-mono uppercase tracking-widest text-sand mt-0.5">Verified Exercises</div>
                  </div>
                  <div>
                    <div className="font-display text-2xl sm:text-3xl font-bold text-chalk tabular-nums">&lt; 200ms</div>
                    <div className="text-[11px] font-mono uppercase tracking-widest text-sand mt-0.5">Safety Pre-Check</div>
                  </div>
                </div>
              </div>

              {/* ATHLETIC HUD PREVIEW TILE */}
              <div className="lg:col-span-5">
                <div className="rounded-md border border-forest bg-carbon-surface p-6 shadow-2xl space-y-6">
                  <div className="flex items-center justify-between border-b border-forest/80 pb-4">
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 bg-lime animate-ping" />
                      <span className="text-xs font-mono uppercase tracking-widest text-chalk">
                        SESSION TELEMETRY // ACTIVE
                      </span>
                    </div>
                    <Badge variant="forest">STAGE: ONBOARDED</Badge>
                  </div>

                  {/* Stat HUD */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-forest/20 p-4 rounded-sm border border-forest/40">
                      <div className="text-[10px] font-mono uppercase tracking-wider text-sand">Cycle Consistency</div>
                      <div className="font-display text-2xl font-bold text-lime tabular-nums mt-1">94.2%</div>
                      <div className="text-[10px] font-mono text-sand/80 mt-1">14 of 15 scheduled sessions</div>
                    </div>
                    <div className="bg-forest/20 p-4 rounded-sm border border-forest/40">
                      <div className="text-[10px] font-mono uppercase tracking-wider text-sand">Mean RPE Load</div>
                      <div className="font-display text-2xl font-bold text-chalk tabular-nums mt-1">7.4 / 10</div>
                      <div className="text-[10px] font-mono text-sand/80 mt-1">Target range maintained</div>
                    </div>
                  </div>

                  {/* Scheduled Prescription */}
                  <div className="border border-forest/60 p-4 rounded-sm space-y-3">
                    <div className="flex items-center justify-between text-xs font-mono">
                      <span className="text-sand uppercase">TODAY&apos;S PRESCRIPTION</span>
                      <span className="text-lime font-semibold">45 MINS</span>
                    </div>
                    <div className="font-display font-semibold text-chalk text-base tracking-tight uppercase">
                      POSTERIOR CHAIN HYPERTROPHY &amp; CORE
                    </div>
                    <div className="space-y-1.5 text-xs text-sand/90 font-mono">
                      <div className="flex justify-between border-b border-forest/40 pb-1">
                        <span>01. Barbell Romanian Deadlift</span>
                        <span className="text-chalk font-semibold">4x10 @ RPE 8</span>
                      </div>
                      <div className="flex justify-between border-b border-forest/40 pb-1">
                        <span>02. Bulgarian Split Squat</span>
                        <span className="text-chalk font-semibold">3x12/leg</span>
                      </div>
                      <div className="flex justify-between">
                        <span>03. Anti-Extension Forearm Plank</span>
                        <span className="text-chalk font-semibold">3x45s</span>
                      </div>
                    </div>
                  </div>

                  {/* Safety Guardrail Status */}
                  <div className="flex items-center justify-between bg-forest/30 px-3.5 py-2.5 rounded-sm text-xs font-mono text-sand">
                    <div className="flex items-center gap-2">
                      <ShieldCheck className="h-4 w-4 text-lime" />
                      <span>CLINICAL INVARIANTS:</span>
                    </div>
                    <span className="text-lime font-semibold">ACTIVE &amp; ENFORCED</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* 4 ARCHITECTURAL PILLARS */}
        <section id="methodology" className="py-24 border-b border-forest bg-carbon-surface">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mb-16">
              <Badge variant="sand" className="mb-3">ENGINEERING PRINCIPLES</Badge>
              <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight text-chalk uppercase">
                WHY FEEDGUIDE AI DEPARTS FROM GENERIC SAAS
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              
              <Card>
                <CardHeader>
                  <Database className="h-6 w-6 text-lime mb-2" />
                  <CardTitle>Grounded In Real Data</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-sand leading-relaxed">
                    Every daily workout and chat response is compiled from your actual logged sets, equipment catalog, and schedule status. Zero imaginary exercises.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <ShieldCheck className="h-6 w-6 text-lime mb-2" />
                  <CardTitle>Deterministic Safety</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-sand leading-relaxed">
                    Hardcoded safety module checks for red flags: chest pain, syncope, acute trauma, and eating disorders trigger immediate clinical consultation stops.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <Target className="h-6 w-6 text-lime mb-2" />
                  <CardTitle>Age-Appropriate</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-sand leading-relaxed">
                    Minors under 18 receive form-focused bodyweight and light progression with zero 1RM max-effort lifting. Seniors receive balance and low-impact work.
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <Activity className="h-6 w-6 text-lime mb-2" />
                  <CardTitle>Evidence Citations</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-sand leading-relaxed">
                    A pgvector RAG pipeline cross-references responses against ACSM, NSCA, and WHO public health guidelines with explicit inline citations.
                  </p>
                </CardContent>
              </Card>

            </div>
          </div>
        </section>

        {/* CLINICAL SAFETY SPECIFICATION SPOTLIGHT */}
        <section id="safety" className="py-24 border-b border-forest">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <div className="lg:col-span-5 space-y-4">
                <Badge variant="burnt">STRICT INVARIANTS</Badge>
                <h2 className="font-display text-3xl font-bold tracking-tight text-chalk uppercase">
                  NON-NEGOTIABLE CLINICAL GUARDRAILS
                </h2>
                <p className="text-sm text-sand leading-relaxed">
                  Most AI fitness tools hallucinate dangerous advice when users report pain or ask for extreme diets. FeedGuide AI embeds deterministic rule checks before and after every LLM generation.
                </p>
                <ul className="space-y-3 pt-2 text-sm text-chalk font-mono">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-lime" />
                    <span>No medical diagnosis or clinical treatment</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-lime" />
                    <span>Zero max-effort lifting for youth athletes</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-lime" />
                    <span>No extreme caloric deficits or appearance scoring</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-lime" />
                    <span>Immediate cessation for chest pain &amp; dizziness</span>
                  </li>
                </ul>
              </div>

              <div className="lg:col-span-7">
                <div className="border border-burnt/40 bg-carbon-surface rounded-md p-6 font-mono text-xs space-y-4">
                  <div className="flex items-center justify-between text-sand border-b border-forest pb-2">
                    <span>SAFETY SIMULATION // INPUT TEST</span>
                    <span className="text-burnt uppercase">STATUS: INTERCEPTED</span>
                  </div>
                  <div className="bg-carbon p-3 rounded-sm border border-forest">
                    <span className="text-sand/70">ATHLETE QUERY:</span>
                    <p className="text-chalk mt-1">&quot;I felt sharp chest pain and dizziness during squats, should I push through set 4?&quot;</p>
                  </div>
                  <div className="bg-burnt/10 border border-burnt/40 p-4 rounded-sm text-chalk space-y-2">
                    <div className="flex items-center gap-2 text-burnt font-semibold">
                      <ShieldCheck className="h-4 w-4" />
                      <span>CRITICAL INVARIANT TRIGGERED: [cardiac_warning]</span>
                    </div>
                    <p className="text-sand leading-relaxed">
                      Chest pain or tightness requires immediate clinical medical attention. Stop all physical activity immediately and contact emergency medical services or a physician. Workout plan generation has been halted.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

      </main>

      <Footer />
    </div>
  );
}
