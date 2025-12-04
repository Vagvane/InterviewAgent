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
import { User, Mail, Save, Loader2 } from "lucide-react"

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
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

    // Form state
    const [fullName, setFullName] = useState("")
    const [email, setEmail] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, userRes] = await Promise.all([
                    api.get("/profile/stats"),
                    api.get("/users/me")
                ])
                setStats(statsRes.data)
                setUser(userRes.data)
                setFullName(userRes.data.full_name || "")
                setEmail(userRes.data.email || "")
            } catch (error) {
                console.error("Failed to fetch data", error)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    const handleSaveProfile = async () => {
        setSaving(true)
        setMessage(null)
        try {
            await api.put("/users/me", {
                full_name: fullName,
                email: email
            })
            setMessage({ type: 'success', text: 'Profile updated successfully!' })
            // Update local user state if needed, or trigger a re-fetch in layout context (complex without global state)
            // For now, just reload the page to reflect changes in header is simplest, or just let user know.
            // A full reload is jarring, so we'll just show success. 
            // The header won't update until refresh, which is a known limitation without context/redux.
            // We can force a reload after a short delay if we want.
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

            <Card>
                <CardHeader>
                    <CardTitle>Skills Assessment</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        {Object.entries(stats?.skills_analysis || {}).map(([skill, level]: [string, any]) => (
                            <div key={skill} className="p-4 border rounded-lg bg-gray-50 dark:bg-gray-800">
                                <h4 className="font-bold text-lg">{skill}</h4>
                                <p className="text-blue-600">{level}</p>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
