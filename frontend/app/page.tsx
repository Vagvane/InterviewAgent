"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"
import { CheckCircle, Code, Video, BookOpen, ArrowRight, Star, Zap, Shield } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col overflow-hidden">
      {/* Modern Glass Header */}
      <header className="fixed top-0 w-full z-50 glass border-b-0">
        <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
          <Link href="/">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20">
                IA
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
                Interview Agent
              </span>
            </div>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost" className="text-muted-foreground hover:text-foreground">Login</Button>
            </Link>
            <Link href="/signup">
              <Button className="shadow-soft hover:shadow-lg transition-all duration-300">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 pt-16">
        {/* Hero Section */}
        <section className="relative w-full py-24 md:py-32 lg:py-40 flex flex-col items-center text-center px-4 overflow-hidden">
          {/* Background Blobs */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-gradient-to-b from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20 rounded-[100%] blur-3xl -z-10 opacity-60" />

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="max-w-4xl space-y-8 relative z-10"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/50 dark:bg-white/5 border border-white/20 shadow-sm backdrop-blur-sm mb-4">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              <span className="text-sm font-medium text-muted-foreground">AI-Powered Interview Prep</span>
            </div>

            <h1 className="text-6xl md:text-8xl font-bold tracking-tight text-gray-900 dark:text-white leading-[1.1]">
              Master Your <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 animate-gradient-x">
                Tech Interview
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Unlock your potential with AI-driven assessments, real-time coding challenges, and realistic mock interviews.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
              <Link href="/signup">
                <Button size="lg" className="h-14 px-8 text-lg rounded-full shadow-soft hover:shadow-xl hover:-translate-y-1 transition-all duration-300 bg-gradient-to-r from-blue-600 to-purple-600 border-0">
                  Start Practicing Free <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="#features">
                <Button size="lg" variant="outline" className="h-14 px-8 text-lg rounded-full border-2 hover:bg-secondary/50 backdrop-blur-sm">
                  How it Works
                </Button>
              </Link>
            </div>
          </motion.div>
        </section>

        {/* Features Bento Grid */}
        <section id="features" className="w-full py-24 px-4 bg-secondary/30">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-5xl font-bold mb-6">Everything you need to succeed</h2>
              <p className="text-xl text-muted-foreground">Comprehensive tools designed to help you crack your dream job.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[300px]">
              {/* Large Card */}
              <motion.div
                whileHover={{ y: -5 }}
                className="md:col-span-2 row-span-2 p-8 rounded-[2rem] bg-white dark:bg-gray-900 shadow-soft border border-gray-100 dark:border-gray-800 relative overflow-hidden group"
              >
                <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50 dark:bg-blue-900/20 rounded-full blur-3xl -mr-16 -mt-16 transition-all group-hover:bg-blue-100 dark:group-hover:bg-blue-900/30" />
                <div className="relative z-10 h-full flex flex-col justify-between">
                  <div>
                    <div className="h-14 w-14 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-6 text-blue-600">
                      <Code className="h-7 w-7" />
                    </div>
                    <h3 className="text-3xl font-bold mb-4">Interactive Coding Arena</h3>
                    <p className="text-lg text-muted-foreground max-w-md">
                      Practice algorithms in a full-featured code editor. Run code against test cases in real-time with support for Python, Java, and C++.
                    </p>
                  </div>
                  <div className="w-full h-48 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm mt-8 overflow-hidden relative">
                    <div className="absolute inset-0 bg-gradient-to-br from-transparent to-gray-100/50 dark:to-gray-800/50" />
                    {/* Mock Code Editor UI */}
                    <div className="p-4 space-y-2 font-mono text-xs text-gray-400">
                      <div className="flex gap-2"><span className="text-purple-500">def</span> <span className="text-blue-500">solve</span>(nums, target):</div>
                      <div className="pl-4"><span className="text-gray-500"># Your solution here</span></div>
                      <div className="pl-4"><span className="text-purple-500">return</span> []</div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Tall Card */}
              <motion.div
                whileHover={{ y: -5 }}
                className="row-span-2 p-8 rounded-[2rem] bg-white dark:bg-gray-900 shadow-soft border border-gray-100 dark:border-gray-800 relative overflow-hidden group"
              >
                <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-purple-50 to-transparent dark:from-purple-900/20 opacity-50" />
                <div className="relative z-10 h-full flex flex-col">
                  <div className="h-14 w-14 rounded-2xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-6 text-purple-600">
                    <Video className="h-7 w-7" />
                  </div>
                  <h3 className="text-3xl font-bold mb-4">AI Mock Interviews</h3>
                  <p className="text-lg text-muted-foreground mb-8">
                    Experience realistic voice interviews with our AI avatar. It listens, speaks, and adapts to your answers just like a real interviewer.
                  </p>
                  <div className="flex-1 flex items-center justify-center">
                    <div className="relative w-32 h-32 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 animate-pulse flex items-center justify-center shadow-lg shadow-purple-500/30">
                      <div className="w-28 h-28 rounded-full bg-white dark:bg-gray-900 flex items-center justify-center">
                        <div className="w-20 h-20 rounded-full bg-gray-100 dark:bg-gray-800" />
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Small Card 1 */}
              <motion.div
                whileHover={{ y: -5 }}
                className="p-8 rounded-[2rem] bg-white dark:bg-gray-900 shadow-soft border border-gray-100 dark:border-gray-800 relative overflow-hidden group"
              >
                <div className="h-12 w-12 rounded-2xl bg-pink-100 dark:bg-pink-900/30 flex items-center justify-center mb-4 text-pink-600">
                  <BookOpen className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold mb-2">Daily Assessments</h3>
                <p className="text-muted-foreground">Keep your knowledge fresh with personalized quizzes generated daily.</p>
              </motion.div>

              {/* Small Card 2 */}
              <motion.div
                whileHover={{ y: -5 }}
                className="p-8 rounded-[2rem] bg-white dark:bg-gray-900 shadow-soft border border-gray-100 dark:border-gray-800 relative overflow-hidden group"
              >
                <div className="h-12 w-12 rounded-2xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center mb-4 text-green-600">
                  <Zap className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-bold mb-2">Instant Feedback</h3>
                <p className="text-muted-foreground">Get detailed analysis and improvements immediately after every session.</p>
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="w-full py-24 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="p-12 rounded-[3rem] bg-gradient-to-br from-gray-900 to-gray-800 text-white shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl -mr-20 -mt-20" />
              <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl -ml-20 -mb-20" />

              <div className="relative z-10 space-y-8">
                <h2 className="text-4xl md:text-5xl font-bold">Ready to ace your interview?</h2>
                <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                  Join thousands of developers who are upgrading their careers with Interview Agent.
                </p>
                <Link href="/signup">
                  <Button size="lg" className="h-14 px-10 text-lg rounded-full bg-white text-gray-900 hover:bg-gray-100 border-0 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300">
                    Get Started Now
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="py-12 text-center text-sm text-muted-foreground bg-secondary/30">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <p>© 2025 Interview Agent. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="#" className="hover:text-foreground transition-colors">Privacy</Link>
            <Link href="#" className="hover:text-foreground transition-colors">Terms</Link>
            <Link href="#" className="hover:text-foreground transition-colors">Contact</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
