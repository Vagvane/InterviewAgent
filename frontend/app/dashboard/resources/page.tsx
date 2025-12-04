"use client"

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Video, FileText, ExternalLink, PlayCircle } from "lucide-react"
import { motion } from "framer-motion"

const resources = [
    {
        title: "System Design Primer",
        type: "Article",
        category: "System Design",
        description: "A comprehensive guide to distributed systems and scalable architectures.",
        icon: FileText,
        color: "text-blue-600",
        bgColor: "bg-blue-100 dark:bg-blue-900/30",
        link: "#"
    },
    {
        title: "Mastering Dynamic Programming",
        type: "Video Course",
        category: "Algorithms",
        description: "Learn how to solve complex DP problems with step-by-step visualizations.",
        icon: Video,
        color: "text-purple-600",
        bgColor: "bg-purple-100 dark:bg-purple-900/30",
        link: "#"
    },
    {
        title: "Behavioral Interview Cheat Sheet",
        type: "Guide",
        category: "Soft Skills",
        description: "Top 50 behavioral questions and how to answer them using the STAR method.",
        icon: BookOpen,
        color: "text-green-600",
        bgColor: "bg-green-100 dark:bg-green-900/30",
        link: "#"
    },
    {
        title: "React.js Interview Patterns",
        type: "Article",
        category: "Frontend",
        description: "Common patterns and hooks questions asked in senior frontend interviews.",
        icon: FileText,
        color: "text-cyan-600",
        bgColor: "bg-cyan-100 dark:bg-cyan-900/30",
        link: "#"
    },
    {
        title: "Mock Interview: Google L4",
        type: "Video",
        category: "Mock Interview",
        description: "Watch a real mock interview session for a Google L4 Software Engineer role.",
        icon: PlayCircle,
        color: "text-red-600",
        bgColor: "bg-red-100 dark:bg-red-900/30",
        link: "#"
    }
]

export default function ResourcesPage() {
    return (
        <motion.div
            className="max-w-5xl mx-auto space-y-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Learning Resources</h2>
                <p className="text-muted-foreground">Curated materials to help you ace your interviews.</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {resources.map((resource, index) => {
                    const Icon = resource.icon
                    return (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <Card className="h-full border-none shadow-soft hover:shadow-lg transition-all duration-300 group">
                                <CardHeader>
                                    <div className="flex justify-between items-start mb-2">
                                        <div className={`p-3 rounded-xl ${resource.bgColor} ${resource.color}`}>
                                            <Icon className="h-6 w-6" />
                                        </div>
                                        <Badge variant="secondary" className="font-normal">{resource.type}</Badge>
                                    </div>
                                    <CardTitle className="text-xl group-hover:text-blue-600 transition-colors">{resource.title}</CardTitle>
                                    <CardDescription>{resource.category}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-muted-foreground line-clamp-3">
                                        {resource.description}
                                    </p>
                                </CardContent>
                                <CardFooter>
                                    <Button variant="ghost" className="w-full justify-between text-blue-600 hover:text-blue-700 hover:bg-blue-50 group-hover:translate-x-1 transition-all">
                                        Read More <ExternalLink className="h-4 w-4" />
                                    </Button>
                                </CardFooter>
                            </Card>
                        </motion.div>
                    )
                })}
            </div>
        </motion.div>
    )
}
