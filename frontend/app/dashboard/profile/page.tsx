"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import api from "@/lib/api"
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { User, Mail, Save, Loader2, FileText, Download } from "lucide-react"

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

export default function ProfilePage() {
    const [stats, setStats] = useState<any>(null)
    const [user, setUser] = useState<{ email: string; full_name: string | null } | null>(null)
    const [history, setHistory] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [historyLoading, setHistoryLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [activeTab, setActiveTab] = useState('assessments')
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

    // Form state
    const [fullName, setFullName] = useState("")
    const [email, setEmail] = useState("")

    const [fromDate, setFromDate] = useState("")
    const [toDate, setToDate] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, userRes, historyRes] = await Promise.all([
                    api.get("/profile/stats"),
                    api.get("/users/me"),
                    api.get("/profile/history")
                ])
                setStats(statsRes.data)
                setUser(userRes.data)
                setHistory(historyRes.data)
                setFullName(userRes.data.full_name || "")
                setEmail(userRes.data.email || "")
            } catch (error) {
                console.error("Failed to fetch data", error)
            } finally {
                setLoading(false)
                setHistoryLoading(false)
            }
        }
        fetchData()
    }, [])

    const handleViewReport = (type: string, id: number) => {
        let reportType = type;
        if (type === 'assessments') reportType = 'assessment';
        if (type === 'interviews') reportType = 'interview';

        const url = `/report?type=${reportType}&id=${id}`;
        window.open(url, '_blank');
    }

    const handleSaveProfile = async () => {
        setSaving(true)
        setMessage(null)
        try {
            await api.put("/users/me", {
                full_name: fullName,
                email: email
            })
            setMessage({ type: 'success', text: 'Profile updated successfully!' })
            setTimeout(() => {
                window.location.reload()
            }, 1000)
        } catch (error) {
            console.error("Failed to update profile", error)
            setMessage({ type: 'error', text: 'Failed to update profile. Please try again.' })
        } finally {
            setSaving(false)
        }
    }

    if (loading) return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading profile...</div>

    const barData = {
        labels: ['Assessments', 'Coding', 'Interviews'],
        datasets: [
            {
                label: 'Completed Activities',
                data: [
                    stats?.assessments?.total || 0,
                    stats?.coding?.total_submissions || 0,
                    stats?.interviews?.total || 0,
                ],
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
            },
        ],
    };

    const doughnutData = {
        labels: ['Passed', 'Failed'],
        datasets: [
            {
                data: [
                    stats?.coding?.passed || 0,
                    (stats?.coding?.total_submissions || 0) - (stats?.coding?.passed || 0)
                ],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.5)',
                    'rgba(239, 68, 68, 0.5)',
                ],
                borderColor: [
                    'rgba(34, 197, 94, 1)',
                    'rgba(239, 68, 68, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="space-y-8 max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold tracking-tight">Your Profile</h2>

            {/* Profile Edit Card */}
            <Card>
                <CardHeader>
                    <CardTitle>Personal Information</CardTitle>
                    <CardDescription>Update your personal details here.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid gap-2">
                        <Label htmlFor="full_name">Full Name</Label>
                        <div className="relative">
                            <User className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                id="full_name"
                                placeholder="John Doe"
                                className="pl-8"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                            />
                        </div>
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="email">Email</Label>
                        <div className="relative">
                            <Mail className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                id="email"
                                type="email"
                                placeholder="john@example.com"
                                className="pl-8"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                    </div>
                    {message && (
                        <div className={`text-sm ${message.type === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                            {message.text}
                        </div>
                    )}
                </CardContent>
                <CardFooter>
                    <Button onClick={handleSaveProfile} disabled={saving} className="cursor-pointer">
                        {saving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                        Save Changes
                    </Button>
                </CardFooter>
            </Card>

            <h3 className="text-2xl font-bold tracking-tight mt-8">Analytics Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Activity Overview</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Bar options={{ responsive: true }} data={barData} />
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Coding Success Rate</CardTitle>
                    </CardHeader>
                    <CardContent className="flex justify-center">
                        <div className="w-64">
                            <Doughnut data={doughnutData} />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* NEW: Activity History Section */}
            <div className="space-y-6">
                <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-bold tracking-tight">Activity History</h3>
                    <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
                        {['assessments', 'coding', 'interviews'].map((tab) => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors capitalize ${activeTab === tab
                                    ? 'bg-white dark:bg-gray-950 shadow-sm text-blue-600'
                                    : 'text-gray-500 hover:text-gray-900 dark:hover:text-gray-300'
                                    }`}
                            >
                                {tab}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="flex gap-4 items-end bg-gray-50 dark:bg-gray-800/50 p-4 rounded-lg">
                    <div className="grid gap-2">
                        <Label htmlFor="fromDate" className="text-xs">From Date</Label>
                        <Input
                            id="fromDate"
                            type="date"
                            className="bg-white dark:bg-gray-800"
                            value={fromDate}
                            onChange={(e) => setFromDate(e.target.value)}
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="toDate" className="text-xs">To Date</Label>
                        <Input
                            id="toDate"
                            type="date"
                            className="bg-white dark:bg-gray-800"
                            value={toDate}
                            onChange={(e) => setToDate(e.target.value)}
                        />
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => { setFromDate(""); setToDate("") }}
                        className="mb-[2px]"
                        disabled={!fromDate && !toDate}
                    >
                        Clear
                    </Button>
                </div>

                <Card>
                    <CardContent className="p-0">
                        {historyLoading ? (
                            <div className="p-8 text-center text-muted-foreground">Loading history...</div>
                        ) : (
                            <div className="relative overflow-x-auto">
                                <table className="w-full text-sm text-left">
                                    <thead className="text-xs uppercase bg-gray-50 dark:bg-gray-800 text-gray-700 dark:text-gray-300">
                                        <tr>
                                            <th className="px-6 py-3">Date</th>
                                            <th className="px-6 py-3">Title</th>
                                            <th className="px-6 py-3">Score/Status</th>
                                            <th className="px-6 py-3 text-right">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {history?.[activeTab]?.filter((item: any) => {
                                            if (!fromDate && !toDate) return true;
                                            const itemDate = new Date(item.date);
                                            const start = fromDate ? new Date(fromDate) : new Date(0);
                                            const end = toDate ? new Date(toDate) : new Date(8640000000000000);
                                            // Reset time parts
                                            start.setHours(0, 0, 0, 0);
                                            end.setHours(23, 59, 59, 999);
                                            return itemDate >= start && itemDate <= end;
                                        }).length > 0 ? (
                                            history[activeTab]
                                                .filter((item: any) => {
                                                    if (!fromDate && !toDate) return true;
                                                    const itemDate = new Date(item.date);
                                                    const start = fromDate ? new Date(fromDate) : new Date(0);
                                                    const end = toDate ? new Date(toDate) : new Date(8640000000000000);
                                                    start.setHours(0, 0, 0, 0);
                                                    end.setHours(23, 59, 59, 999);
                                                    return itemDate >= start && itemDate <= end;
                                                })
                                                .map((item: any) => (
                                                    <tr key={item.id} className="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                                                        <td className="px-6 py-4 font-medium">{item.date}</td>
                                                        <td className="px-6 py-4">{item.title}</td>
                                                        <td className="px-6 py-4">
                                                            <span className={`px-2 py-1 rounded-full text-xs font-semibold ${item.status === 'Passed' || item.status === 'Completed' ? 'bg-green-100 text-green-700' :
                                                                item.status === 'active' ? 'bg-blue-100 text-blue-700' :
                                                                    'bg-gray-100 text-gray-700'
                                                                }`}>
                                                                {item.score || item.status}
                                                            </span>
                                                        </td>
                                                        <td className="px-6 py-4 text-right">
                                                            <Button
                                                                variant="ghost"
                                                                size="sm"
                                                                onClick={() => handleViewReport(activeTab, item.id)}
                                                                className="text-blue-600 hover:text-blue-800 cursor-pointer"
                                                            >
                                                                <Download className="h-4 w-4 mr-2" />
                                                                View Report
                                                            </Button>
                                                        </td>
                                                    </tr>
                                                ))
                                        ) : (
                                            <tr>
                                                <td colSpan={4} className="px-6 py-8 text-center text-muted-foreground">
                                                    No {activeTab} found{fromDate || toDate ? " in this date range" : ""}.
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
