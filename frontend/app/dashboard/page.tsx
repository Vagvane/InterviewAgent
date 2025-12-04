"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Activity, Code, Trophy, Clock, Play, Video, BookOpen, Download, HelpCircle, BarChart2, Calendar, ArrowUpRight, Sparkles, Settings, FileText } from "lucide-react"
import api from "@/lib/api"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { motion } from "framer-motion"

export default function DashboardPage() {
    const [stats, setStats] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [user, setUser] = useState<{ full_name: string } | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, userRes] = await Promise.all([
                    api.get("/profile/stats"),
                    api.get("/users/me")
                ])
                setStats(statsRes.data)
                setUser(userRes.data)
            } catch (error) {
                console.error("Failed to fetch data", error)
                setError("Failed to load data. Please check backend connection.")
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })

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

    if (loading) return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading dashboard data...</div>
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>

    return (
        <motion.div
            className="space-y-8"
            variants={container}
            initial="hidden"
            animate="show"
        >
            {/* Welcome Header */}
            <motion.div variants={item} className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Welcome back, {user?.full_name || "User"}!</h2>
                    <p className="text-muted-foreground mt-1 flex items-center gap-2">
                        <Calendar className="h-4 w-4" /> {currentDate}
                    </p>
                </div>
                <div className="flex gap-3">
                    <Link href="/dashboard/assessment">
                        <Button className="shadow-soft bg-gradient-to-r from-blue-600 to-purple-600 border-0 hover:shadow-lg transition-all">
                            <Sparkles className="mr-2 h-4 w-4" /> Daily Challenge
                        </Button>
                    </Link>
                    <Link href="/dashboard/upgrade">
                        <Button variant="outline" className="shadow-sm border-blue-200 text-blue-600 hover:bg-blue-50">
                            Upgrade to Pro
                        </Button>
                    </Link>
                </div>
            </motion.div>

            {/* Stats Section - Floating Cards */}
            <motion.div variants={item}>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    <Card className="border-none shadow-soft bg-white dark:bg-gray-800 hover:-translate-y-1 transition-transform duration-300">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-green-100 dark:bg-green-900/30 text-green-600 rounded-2xl">
                                    <Activity className="h-6 w-6" />
                                </div>
                                <span className="text-xs font-medium px-2 py-1 rounded-full bg-green-50 text-green-600 dark:bg-green-900/20">+2.5%</span>
                            </div>
                            <p className="text-sm text-muted-foreground font-medium">Average Score</p>
                            <h4 className="text-3xl font-bold mt-1">{Math.round(stats?.assessments?.average_score || 0)}%</h4>
                        </CardContent>
                    </Card>
                    <Card className="border-none shadow-soft bg-white dark:bg-gray-800 hover:-translate-y-1 transition-transform duration-300">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-2xl">
                                    <Trophy className="h-6 w-6" />
                                </div>
                                <span className="text-xs font-medium px-2 py-1 rounded-full bg-blue-50 text-blue-600 dark:bg-blue-900/20">Level 5</span>
                            </div>
                            <p className="text-sm text-muted-foreground font-medium">Assignments Completed</p>
                            <h4 className="text-3xl font-bold mt-1">{stats?.total_completed || 0}</h4>
                        </CardContent>
                    </Card>
                    <Card className="border-none shadow-soft bg-white dark:bg-gray-800 hover:-translate-y-1 transition-transform duration-300">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-orange-100 dark:bg-orange-900/30 text-orange-600 rounded-2xl">
                                    <Video className="h-6 w-6" />
                                </div>
                                <span className="text-xs font-medium px-2 py-1 rounded-full bg-orange-50 text-orange-600 dark:bg-orange-900/20">New</span>
                            </div>
                            <p className="text-sm text-muted-foreground font-medium">Interviews Done</p>
                            <h4 className="text-3xl font-bold mt-1">{stats?.interviews?.total || 0}</h4>
                        </CardContent>
                    </Card>
                    <Card className="border-none shadow-soft bg-white dark:bg-gray-800 hover:-translate-y-1 transition-transform duration-300">
                        <CardContent className="p-6">
                            <div className="flex justify-between items-start mb-4">
                                <div className="p-3 bg-purple-100 dark:bg-purple-900/30 text-purple-600 rounded-2xl">
                                    <Clock className="h-6 w-6" />
                                </div>
                            </div>
                            <p className="text-sm text-muted-foreground font-medium">Study Hours</p>
                            <h4 className="text-3xl font-bold mt-1">12h</h4>
                        </CardContent>
                    </Card>
                </div>
            </motion.div>

            {/* Action Cards - Modern Grid */}
            <motion.div variants={item}>
                <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Start Practicing</h3>
                <div className="grid gap-6 md:grid-cols-3">
                    {/* Daily Assessment */}
                    <Link href="/dashboard/assessment" className="group">
                        <Card className="h-full border-none shadow-soft hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 overflow-hidden relative">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 dark:bg-blue-900/20 rounded-full blur-2xl -mr-10 -mt-10 transition-all group-hover:bg-blue-100 dark:group-hover:bg-blue-900/30" />
                            <CardHeader>
                                <div className="h-12 w-12 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4 text-blue-600 group-hover:scale-110 transition-transform">
                                    <BookOpen className="h-6 w-6" />
                                </div>
                                <CardTitle className="text-xl">Daily Assessment</CardTitle>
                                <CardDescription>Test your knowledge with AI-generated quizzes.</CardDescription>
                            </CardHeader>
                            <CardFooter>
                                <div className="flex items-center text-blue-600 font-medium text-sm group-hover:translate-x-1 transition-transform">
                                    Start Now <ArrowUpRight className="ml-1 h-4 w-4" />
                                </div>
                            </CardFooter>
                        </Card>
                    </Link>

                    {/* Coding Assignments */}
                    <Link href="/dashboard/coding" className="group">
                        <Card className="h-full border-none shadow-soft hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 overflow-hidden relative">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-50 dark:bg-purple-900/20 rounded-full blur-2xl -mr-10 -mt-10 transition-all group-hover:bg-purple-100 dark:group-hover:bg-purple-900/30" />
                            <CardHeader>
                                <div className="h-12 w-12 rounded-2xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-4 text-purple-600 group-hover:scale-110 transition-transform">
                                    <Code className="h-6 w-6" />
                                </div>
                                <CardTitle className="text-xl">Coding Arena</CardTitle>
                                <CardDescription>Solve algorithmic challenges in real-time.</CardDescription>
                            </CardHeader>
                            <CardFooter>
                                <div className="flex items-center text-purple-600 font-medium text-sm group-hover:translate-x-1 transition-transform">
                                    Start Coding <ArrowUpRight className="ml-1 h-4 w-4" />
                                </div>
                            </CardFooter>
                        </Card>
                    </Link>

                    {/* Video Interviews */}
                    <Link href="/dashboard/interview" className="group">
                        <Card className="h-full border-none shadow-soft hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 overflow-hidden relative">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-pink-50 dark:bg-pink-900/20 rounded-full blur-2xl -mr-10 -mt-10 transition-all group-hover:bg-pink-100 dark:group-hover:bg-pink-900/30" />
                            <CardHeader>
                                <div className="h-12 w-12 rounded-2xl bg-pink-100 dark:bg-pink-900/30 flex items-center justify-center mb-4 text-pink-600 group-hover:scale-110 transition-transform">
                                    <Video className="h-6 w-6" />
                                </div>
                                <CardTitle className="text-xl">Mock Interview</CardTitle>
                                <CardDescription>Practice with our realistic AI interviewer.</CardDescription>
                            </CardHeader>
                            <CardFooter>
                                <div className="flex items-center text-pink-600 font-medium text-sm group-hover:translate-x-1 transition-transform">
                                    Start Interview <ArrowUpRight className="ml-1 h-4 w-4" />
                                </div>
                            </CardFooter>
                        </Card>
                    </Link>
                </div>
            </motion.div>

            {/* Performance Overview & Quick Actions */}
            <motion.div variants={item} className="grid md:grid-cols-3 gap-6">
                <Card className="md:col-span-2 border-none shadow-soft bg-white dark:bg-gray-800">
                    <CardHeader>
                        <CardTitle className="text-lg">Performance Overview</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-6">
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="font-medium">Overall Progress</span>
                                    <span className="text-muted-foreground">32%</span>
                                </div>
                                <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" style={{ width: '32%' }}></div>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="font-medium">Score Trend</span>
                                    <span className="text-muted-foreground">+12%</span>
                                </div>
                                <div className="h-3 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div className="h-full bg-gradient-to-r from-green-400 to-emerald-500 rounded-full" style={{ width: '65%' }}></div>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Link href="/dashboard/report" className="w-full">
                            <Button variant="ghost" className="w-full text-blue-600 hover:text-blue-700 hover:bg-blue-50 cursor-pointer">View Detailed Report</Button>
                        </Link>
                    </CardFooter>
                </Card>

                <Card className="border-none shadow-soft bg-white dark:bg-gray-800">
                    <CardHeader>
                        <CardTitle className="text-lg">Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        <Link href="/dashboard/leaderboard">
                            <Button variant="outline" className="w-full justify-start h-12 border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all mb-3">
                                <Trophy className="mr-2 h-4 w-4 text-yellow-500" />
                                <span>View Leaderboard</span>
                            </Button>
                        </Link>
                        <Link href="/dashboard/report">
                            <Button variant="outline" className="w-full justify-start h-12 border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all mb-3">
                                <Download className="mr-2 h-4 w-4 text-blue-500" />
                                <span>Download Report</span>
                            </Button>
                        </Link>
                        <Link href="/dashboard/resources">
                            <Button variant="outline" className="w-full justify-start h-12 border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all mb-3">
                                <BookOpen className="mr-2 h-4 w-4 text-purple-500" />
                                <span>View Resources</span>
                            </Button>
                        </Link>
                        <Link href="/dashboard/settings">
                            <Button variant="outline" className="w-full justify-start h-12 border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-all">
                                <Settings className="mr-2 h-4 w-4 text-gray-500" />
                                <span>Settings</span>
                            </Button>
                        </Link>
                    </CardContent>
                </Card>
            </motion.div>
        </motion.div>
    )
}
