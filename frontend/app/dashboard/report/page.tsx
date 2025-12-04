"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download, TrendingUp, Award, Target, Calendar } from "lucide-react"
import { useRouter } from "next/navigation"
import api from "@/lib/api"
import { motion } from "framer-motion"

export default function ReportPage() {
    const router = useRouter()
    const [stats, setStats] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await api.get("/profile/stats")
                setStats(res.data)
            } catch (error) {
                console.error("Failed to fetch stats", error)
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    if (loading) return <div className="p-10 text-center">Generating Report...</div>

    const getSkillColor = (level: string) => {
        switch (level) {
            case "Advanced": return "text-green-600 bg-green-50 border-green-200"
            case "Intermediate": return "text-blue-600 bg-blue-50 border-blue-200"
            default: return "text-gray-600 bg-gray-50 border-gray-200"
        }
    }

    return (
        <div className="max-w-5xl mx-auto space-y-8 p-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" size="icon" onClick={() => router.back()}>
                        <ArrowLeft className="h-5 w-5" />
                    </Button>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Performance Report</h1>
                        <p className="text-muted-foreground">Comprehensive analysis of your interview readiness.</p>
                    </div>
                </div>
                <Button variant="outline" className="gap-2">
                    <Download className="h-4 w-4" /> Export PDF
                </Button>
            </div>

            {/* Overview Cards */}
            <div className="grid gap-6 md:grid-cols-4">
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Overall Score</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">{Math.round(stats?.assessments?.average_score || 0)}%</div>
                        <p className="text-xs text-muted-foreground mt-1">+2.5% from last week</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Coding Problems</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">{stats?.coding?.passed || 0}</div>
                        <p className="text-xs text-muted-foreground mt-1">Solved Successfully</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Interviews</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">{stats?.interviews?.total || 0}</div>
                        <p className="text-xs text-muted-foreground mt-1">Sessions Completed</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Study Streak</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">3 Days</div>
                        <p className="text-xs text-muted-foreground mt-1">Keep it up!</p>
                    </CardContent>
                </Card>
            </div>

            {/* Skills Analysis */}
            <Card className="border-none shadow-md">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Target className="h-5 w-5 text-blue-500" />
                        Skills Assessment
                    </CardTitle>
                    <CardDescription>AI-driven analysis of your technical competencies.</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-4 md:grid-cols-3">
                        {Object.entries(stats?.skills_analysis || {}).map(([skill, level]: [string, any]) => (
                            <div key={skill} className={`p-4 rounded-xl border ${getSkillColor(level)} flex flex-col items-center text-center gap-2`}>
                                <span className="font-semibold text-lg">{skill}</span>
                                <span className="text-sm px-3 py-1 rounded-full bg-white/50 font-medium">{level}</span>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Detailed Activity Log (Mock for now, but structure is ready) */}
            <Card className="border-none shadow-md">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Calendar className="h-5 w-5 text-purple-500" />
                        Recent Activity
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                                <div className="flex items-center gap-4">
                                    <div className="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600">
                                        <Award className="h-5 w-5" />
                                    </div>
                                    <div>
                                        <p className="font-medium">Completed Daily Assessment</p>
                                        <p className="text-sm text-muted-foreground">Score: 85% • 2 hours ago</p>
                                    </div>
                                </div>
                                <Button variant="ghost" size="sm">View</Button>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
