"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, FileText, Code, Video, User, LogOut, Bell, Settings, Menu } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useState, useEffect } from "react"
import api from "@/lib/api"

const sidebarItems = [
    { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
    { icon: FileText, label: "Assessment", href: "/dashboard/assessment" },
    { icon: Code, label: "Coding Arena", href: "/dashboard/coding" },
    { icon: Video, label: "Interview", href: "/dashboard/interview" },
]

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const pathname = usePathname()
    const router = useRouter()
    const [user, setUser] = useState<{ email: string; full_name: string | null } | null>(null)
    const [mounted, setMounted] = useState(false)

    useEffect(() => {
        setMounted(true)
        api.get("/users/me")
            .then((res) => {
                setUser(res.data)
            })
            .catch((err) => {
                console.error("Failed to fetch user info", err)
            })
    }, [])

    const handleLogout = () => {
        localStorage.removeItem("token")
        router.push("/login")
    }

    // Prevent hydration mismatch by not rendering user-specific data until mounted
    const userInitials = mounted && user
        ? (user.full_name ? user.full_name.substring(0, 2).toUpperCase() : (user.email ? user.email.substring(0, 2).toUpperCase() : "US"))
        : "US"

    const userName = mounted && user ? (user.full_name || "User") : "User"
    const userEmail = mounted && user ? (user.email || "user@example.com") : "user@example.com"

    return (
        <div className="flex h-screen bg-background overflow-hidden">
            {/* Sidebar - Floating Glass Style */}
            <aside className="w-72 hidden md:flex flex-col p-4 z-20">
                <div className="h-full rounded-3xl bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl border border-white/20 shadow-soft flex flex-col">
                    <div className="p-6 flex items-center gap-3">
                        <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20">
                            IA
                        </div>
                        <Link href="/">
                            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400 cursor-pointer">
                                Interview Agent
                            </h1>
                        </Link>
                    </div>

                    <nav className="flex-1 px-4 space-y-2 mt-4">
                        {sidebarItems.map((item) => {
                            const Icon = item.icon
                            const isActive = pathname === item.href
                            return (
                                <Link key={item.href} href={item.href}>
                                    <Button
                                        variant="ghost"
                                        className={cn(
                                            "w-full justify-start gap-3 font-medium cursor-pointer h-12 rounded-xl transition-all duration-300",
                                            isActive
                                                ? "bg-white dark:bg-gray-800 text-blue-600 shadow-sm"
                                                : "text-muted-foreground hover:bg-white/50 dark:hover:bg-gray-800/50 hover:text-foreground"
                                        )}
                                    >
                                        <Icon className={cn("h-5 w-5 transition-colors", isActive ? "text-blue-600" : "text-muted-foreground")} />
                                        {item.label}
                                    </Button>
                                </Link>
                            )
                        })}
                    </nav>

                    <div className="p-4 mt-auto">
                        <div className="rounded-2xl bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-4 border border-blue-100 dark:border-blue-900/50">
                            <h4 className="font-semibold text-sm mb-1">Pro Plan</h4>
                            <p className="text-xs text-muted-foreground mb-3">Get unlimited AI interviews</p>
                            <Button size="sm" className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-sm rounded-lg h-8 text-xs">Upgrade</Button>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content Wrapper */}
            <div className="flex-1 flex flex-col overflow-hidden relative">
                {/* Background Decor */}
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-50/50 via-white to-purple-50/50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 -z-10" />

                {/* Top Header */}
                <header className="h-20 flex items-center justify-between px-8 z-10">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" className="md:hidden rounded-xl bg-white/50 backdrop-blur-sm border border-white/20">
                            <Menu className="h-5 w-5" />
                        </Button>
                        <div className="text-sm text-muted-foreground hidden md:block">
                            {/* Breadcrumbs could go here */}
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" className="rounded-full hover:bg-white/50 dark:hover:bg-gray-800/50 transition-colors">
                            <Bell className="h-5 w-5 text-muted-foreground" />
                        </Button>

                        {mounted ? (
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="ghost" className="relative h-10 w-10 rounded-full cursor-pointer p-0 ring-2 ring-white dark:ring-gray-800 shadow-sm">
                                        <Avatar className="h-10 w-10">
                                            <AvatarImage src="/avatars/01.png" alt="@user" />
                                            <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white font-medium">
                                                {userInitials}
                                            </AvatarFallback>
                                        </Avatar>
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent className="w-56 rounded-xl shadow-xl border-none bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl p-2" align="end" forceMount>
                                    <DropdownMenuLabel className="font-normal p-2">
                                        <div className="flex flex-col space-y-1">
                                            <p className="text-sm font-medium leading-none">{userName}</p>
                                            <p className="text-xs leading-none text-muted-foreground">
                                                {userEmail}
                                            </p>
                                        </div>
                                    </DropdownMenuLabel>
                                    <DropdownMenuSeparator className="bg-gray-200 dark:bg-gray-700" />
                                    <DropdownMenuItem className="cursor-pointer rounded-lg focus:bg-blue-50 dark:focus:bg-blue-900/20 focus:text-blue-600" onClick={() => router.push('/dashboard/profile')}>
                                        <User className="mr-2 h-4 w-4" />
                                        <span>Profile</span>
                                    </DropdownMenuItem>
                                    <DropdownMenuItem className="cursor-pointer rounded-lg focus:bg-blue-50 dark:focus:bg-blue-900/20 focus:text-blue-600">
                                        <Settings className="mr-2 h-4 w-4" />
                                        <span>Settings</span>
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator className="bg-gray-200 dark:bg-gray-700" />
                                    <DropdownMenuItem className="text-red-600 cursor-pointer rounded-lg focus:bg-red-50 dark:focus:bg-red-900/20" onClick={handleLogout}>
                                        <LogOut className="mr-2 h-4 w-4" />
                                        <span>Log out</span>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        ) : (
                            <div className="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse" />
                        )}
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto px-8 pb-8">
                    {children}
                </main>
            </div>
        </div>
    )
}
