"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Trophy, Medal, Award, ArrowUp, ArrowDown, Minus } from "lucide-react"
import { motion } from "framer-motion"

const leaderboardData = [
    { rank: 1, name: "Alex Johnson", score: 9850, change: "up" },
    { rank: 2, name: "Sarah Williams", score: 9720, change: "up" },
    { rank: 3, name: "Michael Chen", score: 9650, change: "down" },
    { rank: 4, name: "Emma Davis", score: 9400, change: "same" },
    { rank: 5, name: "David Miller", score: 9350, change: "up" },
    { rank: 6, name: "You", score: 8200, change: "up", isUser: true },
    { rank: 7, name: "James Wilson", score: 8150, change: "down" },
]

export default function LeaderboardPage() {
    return (
        <motion.div
            className="max-w-4xl mx-auto space-y-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Leaderboard</h2>
                    <p className="text-muted-foreground">Top performers this week</p>
                </div>
                <div className="flex gap-2">
                    <div className="bg-yellow-100 text-yellow-700 px-4 py-2 rounded-full font-medium flex items-center gap-2">
                        <Trophy className="h-4 w-4" />
                        Your Rank: #6
                    </div>
                </div>
            </div>

            <Card className="border-none shadow-soft overflow-hidden">
                <CardHeader className="bg-gray-50/50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
                    <div className="grid grid-cols-12 text-sm font-medium text-muted-foreground px-4">
                        <div className="col-span-1">Rank</div>
                        <div className="col-span-1">Trend</div>
                        <div className="col-span-6">User</div>
                        <div className="col-span-4 text-right">Score</div>
                    </div>
                </CardHeader>
                <CardContent className="p-0">
                    {leaderboardData.map((user, index) => (
                        <motion.div
                            key={user.rank}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className={`grid grid-cols-12 items-center p-4 border-b border-gray-50 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors ${user.isUser ? 'bg-blue-50/50 dark:bg-blue-900/10' : ''}`}
                        >
                            <div className="col-span-1 font-bold text-gray-500">
                                {user.rank === 1 && <Medal className="h-6 w-6 text-yellow-500" />}
                                {user.rank === 2 && <Medal className="h-6 w-6 text-gray-400" />}
                                {user.rank === 3 && <Medal className="h-6 w-6 text-amber-600" />}
                                {user.rank > 3 && `#${user.rank}`}
                            </div>
                            <div className="col-span-1 flex justify-center">
                                {user.change === 'up' && <ArrowUp className="h-4 w-4 text-green-500" />}
                                {user.change === 'down' && <ArrowDown className="h-4 w-4 text-red-500" />}
                                {user.change === 'same' && <Minus className="h-4 w-4 text-gray-400" />}
                            </div>
                            <div className="col-span-6 flex items-center gap-3">
                                <Avatar className="h-10 w-10 border-2 border-white shadow-sm">
                                    <AvatarFallback>{user.name.substring(0, 2)}</AvatarFallback>
                                </Avatar>
                                <div>
                                    <p className={`font-medium ${user.isUser ? 'text-blue-600' : ''}`}>{user.name} {user.isUser && '(You)'}</p>
                                    <p className="text-xs text-muted-foreground">Level 5 Developer</p>
                                </div>
                            </div>
                            <div className="col-span-4 text-right font-mono font-bold text-lg">
                                {user.score.toLocaleString()}
                            </div>
                        </motion.div>
                    ))}
                </CardContent>
            </Card>
        </motion.div>
    )
}
