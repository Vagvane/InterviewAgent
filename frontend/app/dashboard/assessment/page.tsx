"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import api from "@/lib/api"
import { Loader2, CheckCircle, XCircle, RefreshCw } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { cn } from "@/lib/utils"

interface Question {
    text: string
    type: "mcq" | "subjective"
    options: string[]
    category?: string
    correct_answer?: string
}

export default function AssessmentPage() {
    const [questions, setQuestions] = useState<Question[]>([])
    const [loading, setLoading] = useState(true)
    const [responses, setResponses] = useState<Record<number, string>>({})
    const [submitted, setSubmitted] = useState(false)
    const [score, setScore] = useState<number | null>(null)
    const [submitting, setSubmitting] = useState(false)

    const [error, setError] = useState<string | null>(null)

    const fetchQuestions = async (refresh = false) => {
        setLoading(true)
        setSubmitted(false)
        setScore(null)
        setResponses({})
        setError(null)
        try {
            const res = await api.get(`/assessment/daily${refresh ? '?refresh=true' : ''}`)
            setQuestions(res.data.questions)
        } catch (error: any) {
            console.error("Failed to fetch assessment", error)
            const msg = error.response?.data?.detail || "Failed to load assessment. Please try again."
            setError(msg)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchQuestions()
    }, [])

    const handleResponseChange = (index: number, value: string) => {
        setResponses(prev => ({ ...prev, [index]: value }))
    }

    const handleSubmit = async () => {
        setSubmitting(true)
        try {
            // Calculate score locally for instant feedback or use backend return
            // For this implementation, we'll rely on the backend for the official score
            // but use local state for the visual feedback since we have the correct answers.

            const res = await api.post("/assessment/submit", { responses })
            setScore(res.data.score)
            setSubmitted(true)
            window.scrollTo({ top: 0, behavior: 'smooth' })
        } catch (error) {
            console.error("Failed to submit assessment", error)
        } finally {
            setSubmitting(false)
        }
    }

    // Group questions by category
    const groupedQuestions: Record<string, { question: Question, index: number }[]> = {}
    questions.forEach((q, i) => {
        const category = q.category || "General"
        if (!groupedQuestions[category]) {
            groupedQuestions[category] = []
        }
        groupedQuestions[category].push({ question: q, index: i })
    })

    return (
        <div className="max-w-4xl mx-auto space-y-8 pb-12">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Daily Assessment</h2>
                    <p className="text-muted-foreground">
                        {submitted
                            ? `You scored ${score}%! Review your answers below.`
                            : "Complete today's challenge to keep your streak alive."}
                    </p>
                </div>
                {(submitted || error) && (
                    <Button onClick={() => fetchQuestions(true)} className="gap-2 cursor-pointer">
                        <RefreshCw className="h-4 w-4" />
                        {error ? "Try Again" : "Load New Questions"}
                    </Button>
                )}
            </div>

            {loading ? (
                <div className="flex flex-col items-center justify-center min-h-[40vh] space-y-4">
                    <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                    <p className="text-muted-foreground">Loading your daily challenge...</p>
                </div>
            ) : error ? (
                <div className="flex flex-col items-center justify-center min-h-[40vh] space-y-6 text-center px-4 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-xl bg-gray-50/50 dark:bg-gray-900/50">
                    <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-full">
                        <XCircle className="h-10 w-10 text-red-600 dark:text-red-400" />
                    </div>
                    <div className="space-y-2 max-w-md">
                        <h3 className="text-lg font-semibold text-red-700 dark:text-red-400">Generation Failed</h3>
                        <p className="text-muted-foreground text-sm">{error}</p>
                    </div>
                    <Button onClick={() => fetchQuestions(true)} variant="outline" className="gap-2">
                        <RefreshCw className="h-4 w-4" />
                        Retry Generation
                    </Button>
                </div>
            ) : (
                <>
                    {Object.entries(groupedQuestions).map(([category, items], groupIndex) => (
                        <motion.div
                            key={category}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: groupIndex * 0.1 }}
                            className="space-y-6"
                        >
                            <div className="flex items-center gap-4">
                                <h3 className="text-xl font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-4 py-1 rounded-full">
                                    {category}
                                </h3>
                                <div className="h-px flex-1 bg-gray-200 dark:bg-gray-800" />
                            </div>

                            <div className="grid gap-6">
                                {items.map(({ question, index }) => {
                                    const userAnswer = responses[index]
                                    const isCorrect = userAnswer === question.correct_answer
                                    const showFeedback = submitted && question.type === 'mcq'

                                    return (
                                        <Card key={index} className={cn(
                                            "border-l-4 transition-all duration-300",
                                            showFeedback
                                                ? (isCorrect ? "border-l-green-500 bg-green-50/30 dark:bg-green-900/10" : "border-l-red-500 bg-red-50/30 dark:bg-red-900/10")
                                                : "border-l-blue-500 hover:shadow-md"
                                        )}>
                                            <CardHeader>
                                                <CardTitle className="text-lg font-medium flex gap-3">
                                                    <span className="text-muted-foreground">Q{index + 1}.</span>
                                                    <span>{question.text}</span>
                                                </CardTitle>
                                            </CardHeader>
                                            <CardContent>
                                                {question.type === "mcq" ? (
                                                    <RadioGroup
                                                        value={userAnswer}
                                                        onValueChange={(val) => !submitted && handleResponseChange(index, val)}
                                                        className="space-y-3"
                                                    >
                                                        {question.options.map((option, optIndex) => {
                                                            let optionStyle = "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"

                                                            if (submitted) {
                                                                if (option === question.correct_answer) {
                                                                    optionStyle = "border-green-500 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 font-medium"
                                                                } else if (option === userAnswer && !isCorrect) {
                                                                    optionStyle = "border-red-500 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300"
                                                                } else {
                                                                    optionStyle = "opacity-60"
                                                                }
                                                            }

                                                            return (
                                                                <div
                                                                    key={optIndex}
                                                                    onClick={() => !submitted && handleResponseChange(index, option)}
                                                                    className={cn(
                                                                        "flex items-center space-x-3 border rounded-lg p-4 transition-all cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800",
                                                                        optionStyle,
                                                                        !submitted && userAnswer === option && "border-blue-500 bg-blue-50 dark:bg-blue-900/20 ring-1 ring-blue-500"
                                                                    )}>
                                                                    <RadioGroupItem
                                                                        value={option}
                                                                        id={`q${index}-opt${optIndex}`}
                                                                        disabled={submitted}
                                                                        className="mt-0.5" // Align with text top if multi-line
                                                                    />
                                                                    <Label
                                                                        htmlFor={`q${index}-opt${optIndex}`}
                                                                        className="flex-1 cursor-pointer text-base leading-relaxed pointer-events-none" // pointer-events-none to let div handle click
                                                                    >
                                                                        {option}
                                                                    </Label>
                                                                    {submitted && option === question.correct_answer && (
                                                                        <CheckCircle className="h-5 w-5 text-green-600 shrink-0" />
                                                                    )}
                                                                    {submitted && option === userAnswer && !isCorrect && (
                                                                        <XCircle className="h-5 w-5 text-red-600 shrink-0" />
                                                                    )}
                                                                </div>
                                                            )
                                                        })}
                                                    </RadioGroup>
                                                ) : (
                                                    <div className="space-y-4">
                                                        <Textarea
                                                            placeholder="Type your answer here..."
                                                            value={userAnswer || ""}
                                                            onChange={(e) => handleResponseChange(index, e.target.value)}
                                                            disabled={submitted}
                                                            className="min-h-[100px]"
                                                        />
                                                        {submitted && (
                                                            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-800">
                                                                <p className="text-sm font-semibold text-blue-700 dark:text-blue-300 mb-1">Model Answer:</p>
                                                                <p className="text-sm text-gray-700 dark:text-gray-300">{question.correct_answer}</p>
                                                            </div>
                                                        )}
                                                    </div>
                                                )}
                                            </CardContent>
                                        </Card>
                                    )
                                })}
                            </div>
                        </motion.div>
                    ))}

                    {!submitted && (
                        <div className="flex justify-end pt-6">
                            <Button
                                size="lg"
                                onClick={handleSubmit}
                                disabled={submitting}
                                className="w-full md:w-auto min-w-[200px] text-lg cursor-pointer"
                            >
                                {submitting ? (
                                    <>
                                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                        Submitting...
                                    </>
                                ) : (
                                    "Submit Assessment"
                                )}
                            </Button>
                        </div>
                    )}
                </>
            )}
        </div>
    )
}
