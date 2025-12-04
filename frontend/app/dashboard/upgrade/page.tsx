"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, Sparkles, Zap } from "lucide-react"
import { motion } from "framer-motion"

export default function UpgradePage() {
    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    }

    const item = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
    }

    return (
        <motion.div
            className="max-w-5xl mx-auto space-y-8 py-8"
            variants={container}
            initial="hidden"
            animate="show"
        >
            <motion.div variants={item} className="text-center space-y-4">
                <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">Upgrade your Interview Game</h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Unlock unlimited AI interviews, advanced analytics, and premium coding challenges.
                </p>
            </motion.div>

            <motion.div variants={item} className="grid md:grid-cols-3 gap-8 pt-8">
                {/* Free Plan */}
                <Card className="border-none shadow-soft relative overflow-hidden">
                    <CardHeader>
                        <CardTitle className="text-2xl">Free</CardTitle>
                        <CardDescription>Perfect for getting started</CardDescription>
                        <div className="mt-4">
                            <span className="text-4xl font-bold">$0</span>
                            <span className="text-muted-foreground">/month</span>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <ul className="space-y-3 text-sm">
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> 1 AI Interview per day</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Basic Coding Challenges</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Community Support</li>
                        </ul>
                    </CardContent>
                    <CardFooter>
                        <Button variant="outline" className="w-full rounded-full" disabled>Current Plan</Button>
                    </CardFooter>
                </Card>

                {/* Pro Plan */}
                <Card className="border-2 border-blue-600 shadow-xl relative overflow-hidden scale-105 z-10">
                    <div className="absolute top-0 right-0 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-bl-xl">POPULAR</div>
                    <CardHeader>
                        <div className="flex items-center gap-2">
                            <CardTitle className="text-2xl text-blue-600">Pro</CardTitle>
                            <Sparkles className="h-5 w-5 text-yellow-500 fill-yellow-500" />
                        </div>
                        <CardDescription>For serious job seekers</CardDescription>
                        <div className="mt-4">
                            <span className="text-4xl font-bold">$19</span>
                            <span className="text-muted-foreground">/month</span>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <ul className="space-y-3 text-sm">
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-blue-600" /> Unlimited AI Interviews</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-blue-600" /> Advanced Coding Arena</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-blue-600" /> Detailed Performance Analytics</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-blue-600" /> Resume Review</li>
                        </ul>
                    </CardContent>
                    <CardFooter>
                        <Button className="w-full rounded-full bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg transition-all">Upgrade Now</Button>
                    </CardFooter>
                </Card>

                {/* Enterprise Plan */}
                <Card className="border-none shadow-soft relative overflow-hidden">
                    <CardHeader>
                        <CardTitle className="text-2xl">Enterprise</CardTitle>
                        <CardDescription>For teams and organizations</CardDescription>
                        <div className="mt-4">
                            <span className="text-4xl font-bold">$49</span>
                            <span className="text-muted-foreground">/month</span>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <ul className="space-y-3 text-sm">
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Everything in Pro</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Team Management</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Custom Interview Tracks</li>
                            <li className="flex items-center gap-2"><Check className="h-4 w-4 text-green-500" /> Dedicated Support</li>
                        </ul>
                    </CardContent>
                    <CardFooter>
                        <Button variant="outline" className="w-full rounded-full">Contact Sales</Button>
                    </CardFooter>
                </Card>
            </motion.div>
        </motion.div>
    )
}
