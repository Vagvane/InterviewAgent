"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import api from "@/lib/api"
import { VideoOff, Send, Upload, Mic, MicOff, Camera, CameraOff, X } from "lucide-react"
import { cn } from "@/lib/utils"
import { useRouter } from "next/navigation"
import RobotAvatar from "@/components/robot-avatar"
import { motion, AnimatePresence } from "framer-motion"

// Extend Window interface for Web Speech API
declare global {
    interface Window {
        SpeechRecognition: any;
        webkitSpeechRecognition: any;
    }
}

export default function InterviewPage() {
    const router = useRouter()

    // Global State
    const [started, setStarted] = useState(false)
    const [sessionId, setSessionId] = useState<number | null>(null)
    const [messages, setMessages] = useState<any[]>([])
    const [input, setInput] = useState("")
    const [feedback, setFeedback] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    // AV State
    const [isSpeaking, setIsSpeaking] = useState(false)
    const [cameraActive, setCameraActive] = useState(false)
    const [micActive, setMicActive] = useState(false)

    // Form State
    const [jd, setJd] = useState("")
    const [resume, setResume] = useState<File | null>(null)

    // Refs
    const videoRef = useRef<HTMLVideoElement>(null)
    const recognitionRef = useRef<any>(null)
    const messagesEndRef = useRef<HTMLDivElement>(null)

    // Scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (recognitionRef.current) {
                try { recognitionRef.current.stop() } catch (e) { }
            }
            window.speechSynthesis.cancel()
            stopCamera()
        }
    }, [])

    // AV Functions
    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            if (videoRef.current) {
                videoRef.current.srcObject = stream
            }
            setCameraActive(true)
            setMicActive(true)
        } catch (err) {
            console.error("Error accessing camera:", err)
            alert("Could not access camera/microphone. Please check permissions.")
        }
    }

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = (videoRef.current.srcObject as MediaStream).getTracks()
            tracks.forEach(track => track.stop())
            videoRef.current.srcObject = null
        }
        setCameraActive(false)
        setMicActive(false)
    }

    const toggleCamera = () => {
        if (cameraActive) {
            stopCamera()
        } else {
            startCamera()
        }
    }

    const initSpeechRecognition = () => {
        if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
            // alert("Speech Recognition is not supported in this browser.")
            return
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        const recognition = new SpeechRecognition()
        recognition.continuous = false
        recognition.interimResults = false
        recognition.lang = 'en-US'

        recognition.onstart = () => setIsListening(true)
        recognition.onend = () => setIsListening(false)

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript
            setInput(transcript)
            handleSend(transcript) // Auto-send on speech end
        }

        recognitionRef.current = recognition
    }

    const [isListening, setIsListening] = useState(false)

    const speak = (text: string) => {
        window.speechSynthesis.cancel() // Stop previous
        const utterance = new SpeechSynthesisUtterance(text)
        utterance.onstart = () => setIsSpeaking(true)
        utterance.onend = () => {
            setIsSpeaking(false)
            // Auto-listen after AI finishes speaking
            if (recognitionRef.current && micActive) {
                try {
                    recognitionRef.current.start()
                } catch (e) {
                    // Ignore if already started
                }
            }
        }
        window.speechSynthesis.speak(utterance)
    }

    // Handlers
    const handleStart = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        try {
            const formData = new FormData()
            formData.append("job_description", jd)
            if (resume) {
                formData.append("resume", resume)
            }

            const res = await api.post("/interview/start", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            })

            setSessionId(res.data.session_id)
            setStarted(true)
            const introMsg = res.data.message
            setMessages([{ role: "assistant", content: introMsg }])

            // Speak intro after a slight delay
            setTimeout(() => speak(introMsg), 1500)

        } catch (error) {
            console.error("Failed to start interview", error)
        } finally {
            setLoading(false)
        }
    }

    // Initialize AV when started changes to true
    useEffect(() => {
        if (started) {
            const initAV = async () => {
                await new Promise(resolve => setTimeout(resolve, 100))
                await startCamera()
                initSpeechRecognition()
            }
            initAV()
        }
    }, [started])

    const handleSend = async (textOverride?: string) => {
        const textToSend = textOverride || input
        if (!textToSend.trim() || !sessionId) return

        const userMsg = { role: "user", content: textToSend }
        setMessages(prev => [...prev, userMsg])
        setInput("")

        try {
            const res = await api.post(`/interview/${sessionId}/chat`, { message: userMsg.content })
            const aiResponse = res.data.response

            setMessages(prev => [...prev, { role: "assistant", content: aiResponse }])
            speak(aiResponse)
        } catch (error) {
            console.error("Failed to send message", error)
        }
    }

    const handleEndTest = async () => {
        if (!sessionId) return
        try {
            const res = await api.post(`/interview/${sessionId}/end`)
            stopCamera()
            window.speechSynthesis.cancel()
            setFeedback(res.data.feedback)
        } catch (error) {
            console.error("Failed to end interview", error)
            router.push("/dashboard")
        }
    }

    // Render: Feedback View
    if (feedback) {
        return (
            <div className="max-w-4xl mx-auto py-10 space-y-8">
                <Card className="border-none shadow-xl bg-white dark:bg-gray-800">
                    <CardHeader className="text-center pb-2">
                        <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            Interview Analysis
                        </CardTitle>
                        <p className="text-muted-foreground">Here is your performance report based on the session.</p>
                    </CardHeader>
                    <CardContent className="space-y-8">
                        {/* Score Section */}
                        <div className="flex justify-center py-6">
                            <div className="relative h-40 w-40 flex items-center justify-center">
                                <svg className="h-full w-full transform -rotate-90">
                                    <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent" className="text-gray-200 dark:text-gray-700" />
                                    <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent" strokeDasharray={440} strokeDashoffset={440 - (440 * (feedback.score || 0)) / 100} className="text-blue-600 transition-all duration-1000 ease-out" />
                                </svg>
                                <div className="absolute flex flex-col items-center">
                                    <span className="text-4xl font-bold">{feedback.score}%</span>
                                    <span className="text-sm text-muted-foreground">Overall Score</span>
                                </div>
                            </div>
                        </div>

                        {/* Summary */}
                        <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-xl border border-blue-100 dark:border-blue-800">
                            <h3 className="font-semibold text-blue-700 dark:text-blue-300 mb-2">Executive Summary</h3>
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">{feedback.summary}</p>
                        </div>

                        {/* Strengths & Weaknesses Grid */}
                        <div className="grid md:grid-cols-2 gap-6">
                            <div className="space-y-4">
                                <h3 className="font-semibold flex items-center gap-2 text-green-600">
                                    <div className="h-2 w-2 rounded-full bg-green-500" /> Key Strengths
                                </h3>
                                <ul className="space-y-3">
                                    {feedback.strengths?.map((item: string, i: number) => (
                                        <li key={i} className="flex gap-3 bg-green-50 dark:bg-green-900/10 p-3 rounded-lg border border-green-100 dark:border-green-900/30">
                                            <span className="text-green-600 font-bold">•</span>
                                            <span className="text-sm text-gray-700 dark:text-gray-300">{item}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div className="space-y-4">
                                <h3 className="font-semibold flex items-center gap-2 text-orange-600">
                                    <div className="h-2 w-2 rounded-full bg-orange-500" /> Areas for Improvement
                                </h3>
                                <ul className="space-y-3">
                                    {feedback.weaknesses?.map((item: string, i: number) => (
                                        <li key={i} className="flex gap-3 bg-orange-50 dark:bg-orange-900/10 p-3 rounded-lg border border-orange-100 dark:border-orange-900/30">
                                            <span className="text-orange-600 font-bold">•</span>
                                            <span className="text-sm text-gray-700 dark:text-gray-300">{item}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        <div className="pt-6 flex justify-center">
                            <Button size="lg" onClick={() => router.push("/dashboard")} className="min-w-[200px]">
                                Return to Dashboard
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    // Render: Start View
    if (!started) {
        return (
            <div className="max-w-md mx-auto mt-10">
                <Card className="border-none shadow-soft">
                    <CardHeader>
                        <CardTitle>Start New Interview Session</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleStart} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">Job Description</label>
                                <textarea
                                    className="w-full p-2 border rounded-xl bg-background focus:ring-2 focus:ring-blue-500 outline-none"
                                    rows={4}
                                    value={jd}
                                    onChange={(e) => setJd(e.target.value)}
                                    required
                                    placeholder="Paste the job description here..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Resume (Optional)</label>
                                <div className="flex items-center gap-2 border rounded-xl p-2 bg-background">
                                    <Input
                                        type="file"
                                        onChange={(e) => setResume(e.target.files?.[0] || null)}
                                        accept=".pdf,.doc,.docx,.txt"
                                        className="border-none shadow-none"
                                    />
                                    <Upload className="h-4 w-4 text-muted-foreground mr-2" />
                                </div>
                            </div>
                            <Button type="submit" className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg transition-all" disabled={loading}>
                                {loading ? "Initializing..." : "Start Interview"}
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        )
    }

    // Render: Interview View
    return (
        <div className="flex flex-col h-[calc(100vh-100px)] gap-4">
            {/* Main Stage */}
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4 min-h-0">

                {/* AI Avatar Area (Large) */}
                <Card className="lg:col-span-2 bg-slate-950 relative overflow-hidden flex flex-col items-center justify-center border-0 shadow-2xl rounded-3xl">
                    {/* Background Effects */}
                    <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950 to-slate-950" />
                    <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />

                    {/* Robot Avatar */}
                    <div className="relative z-10 scale-125">
                        <RobotAvatar isSpeaking={isSpeaking} isListening={isListening} />
                    </div>

                    <div className="mt-8 z-10 text-center space-y-2">
                        <p className="text-blue-200/80 text-lg font-medium tracking-wide">
                            {isSpeaking ? "AI Interviewer is speaking..." : (isListening ? "Listening..." : "Processing...")}
                        </p>
                        <div className="flex gap-2 justify-center">
                            {isSpeaking && <span className="flex h-2 w-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '0ms' }} />}
                            {isSpeaking && <span className="flex h-2 w-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '150ms' }} />}
                            {isSpeaking && <span className="flex h-2 w-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '300ms' }} />}
                        </div>
                    </div>

                    {/* User Camera (PIP) */}
                    <div className="absolute bottom-6 right-6 w-64 h-48 bg-slate-900 rounded-2xl overflow-hidden border border-slate-700 shadow-2xl">
                        {cameraActive ? (
                            <video ref={videoRef} autoPlay muted playsInline className="w-full h-full object-cover transform scale-x-[-1]" />
                        ) : (
                            <div className="w-full h-full flex flex-col items-center justify-center text-slate-500 bg-slate-800/50 backdrop-blur">
                                <VideoOff className="h-8 w-8 mb-2" />
                                <span className="text-xs">Camera Off</span>
                            </div>
                        )}

                        {/* Camera Controls Overlay */}
                        <div className="absolute bottom-2 left-0 right-0 flex justify-center gap-2 opacity-0 hover:opacity-100 transition-opacity">
                            <Button size="icon" variant="secondary" className="h-8 w-8 rounded-full bg-black/50 hover:bg-black/70 text-white border-none" onClick={toggleCamera}>
                                {cameraActive ? <CameraOff className="h-4 w-4" /> : <Camera className="h-4 w-4" />}
                            </Button>
                        </div>
                    </div>
                </Card>

                {/* Transcript & Controls */}
                <Card className="flex flex-col overflow-hidden border-none shadow-soft rounded-3xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl">
                    <CardHeader className="py-4 border-b bg-white/50 dark:bg-gray-800/50">
                        <CardTitle className="text-sm font-medium flex items-center justify-between">
                            <span className="flex items-center gap-2">
                                <div className={`h-2 w-2 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : 'bg-gray-300'}`} />
                                Live Transcript
                            </span>
                            <Button size="sm" variant="destructive" onClick={handleEndTest} className="h-8 rounded-full px-4">
                                End Interview
                            </Button>
                        </CardTitle>
                    </CardHeader>

                    <CardContent className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-800">
                        {messages.length === 0 && (
                            <div className="text-center text-muted-foreground mt-10">
                                <p>Interview started.</p>
                                <p className="text-sm">The AI will introduce itself shortly.</p>
                            </div>
                        )}
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                            >
                                <div className={cn(
                                    "max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm",
                                    msg.role === "user"
                                        ? "bg-blue-600 text-white rounded-br-none"
                                        : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-bl-none"
                                )}>
                                    {msg.content}
                                </div>
                            </motion.div>
                        ))}
                        <div ref={messagesEndRef} />
                    </CardContent>

                    {/* Controls */}
                    <div className="p-4 border-t bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm space-y-3">
                        <div className="flex gap-2">
                            <Input
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Type your answer..."
                                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                className="bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 rounded-xl focus-visible:ring-blue-500"
                            />
                            <Button size="icon" onClick={() => handleSend()} className="rounded-xl bg-blue-600 hover:bg-blue-700">
                                <Send className="h-4 w-4" />
                            </Button>
                        </div>
                        <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
                            <span className="flex items-center gap-1">
                                {micActive ? <Mic className="h-3 w-3 text-green-500" /> : <MicOff className="h-3 w-3 text-red-500" />}
                                {micActive ? "Microphone Active" : "Microphone Muted"}
                            </span>
                            <span>AI is listening automatically</span>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    )
}
