"use client"

import { useEffect, useState } from "react"
import Editor from "@monaco-editor/react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import api from "@/lib/api"
import { Play, Send, Loader2, Code2, Terminal, RefreshCw, CheckCircle, XCircle } from "lucide-react"
import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"

const LANGUAGES = {
    python: {
        id: "python",
        name: "Python",
        defaultCode: "# Write your Python code here\ndef solution(nums, target):\n    # Your code here\n    pass"
    },
    java: {
        id: "java",
        name: "Java",
        defaultCode: "// Write your Java code here\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your code here\n        return new int[]{};\n    }\n}"
    },
    cpp: {
        id: "cpp",
        name: "C++",
        defaultCode: "// Write your C++ code here\n#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your code here\n        return {};\n    }\n};"
    }
}

export default function CodingPage() {
    const [problem, setProblem] = useState<any>(null)
    const [language, setLanguage] = useState("python")
    const [code, setCode] = useState(LANGUAGES.python.defaultCode)
    const [output, setOutput] = useState("")
    const [analysis, setAnalysis] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [running, setRunning] = useState(false)
    const [submitting, setSubmitting] = useState(false)

    const fetchProblem = async (refresh = false) => {
        setLoading(true)
        setAnalysis(null)
        setOutput("")
        try {
            const res = await api.get(`/coding/daily${refresh ? '?refresh=true' : ''}`)
            setProblem(res.data)
            // Reset code only if refreshing
            if (refresh) {
                setCode(LANGUAGES[language as keyof typeof LANGUAGES].defaultCode)
            }
        } catch (error) {
            console.error("Failed to fetch problem", error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchProblem()
    }, [])

    const handleLanguageChange = (value: string) => {
        setLanguage(value)
        setCode(LANGUAGES[value as keyof typeof LANGUAGES].defaultCode)
    }

    const handleRun = async () => {
        setRunning(true)
        setOutput("Running tests...")
        setAnalysis(null)
        try {
            const res = await api.post("/coding/run", {
                code,
                language,
                problem_id: problem.id
            })
            setOutput(res.data.output)
            if (res.data.analysis) {
                setAnalysis(res.data.analysis)
            }
        } catch (error) {
            setOutput("Error running code. Please try again.")
        } finally {
            setRunning(false)
        }
    }

    const handleSubmit = async () => {
        setSubmitting(true)
        setOutput("Submitting and evaluating...")
        setAnalysis(null)
        try {
            const res = await api.post("/coding/submit", {
                code,
                language,
                problem_id: problem.id
            })
            setOutput(res.data.result)
            if (res.data.analysis) {
                setAnalysis(res.data.analysis)
            }
        } catch (error) {
            setOutput("Error submitting code. Please try again.")
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <p className="text-muted-foreground">Loading coding challenge...</p>
        </div>
    )

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-100px)]">
            {/* Left Panel: Problem & Output */}
            <div className="space-y-6 flex flex-col h-full overflow-hidden">
                <Card className="flex-1 overflow-y-auto border-l-4 border-l-primary shadow-sm">
                    <CardHeader className="pb-4">
                        <div className="flex justify-between items-start">
                            <div>
                                <CardTitle className="text-2xl font-bold flex items-center gap-2">
                                    <Code2 className="h-6 w-6 text-primary" />
                                    {problem?.title}
                                </CardTitle>
                                <div className="mt-3 flex gap-2">
                                    <Badge variant={
                                        problem?.difficulty === 'Easy' ? 'secondary' :
                                            problem?.difficulty === 'Medium' ? 'default' : 'destructive'
                                    }>
                                        {problem?.difficulty}
                                    </Badge>
                                </div>
                            </div>
                            <Button variant="outline" size="sm" onClick={() => fetchProblem(true)} className="gap-2">
                                <RefreshCw className="h-4 w-4" />
                                Next Question
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="prose dark:prose-invert max-w-none text-sm leading-relaxed">
                            <p>{problem?.description}</p>
                        </div>

                        <div className="bg-muted/50 rounded-lg p-4 border">
                            <h4 className="font-semibold mb-3 flex items-center gap-2 text-sm">
                                <Terminal className="h-4 w-4" />
                                Example Test Cases
                            </h4>
                            <div className="space-y-3">
                                {problem?.test_cases?.map((testCase: any, i: number) => (
                                    <div key={i} className="bg-background p-3 rounded border font-mono text-xs">
                                        <div className="grid grid-cols-[60px_1fr] gap-2">
                                            <span className="text-muted-foreground">Input:</span>
                                            <span className="text-primary">{testCase.input}</span>
                                            <span className="text-muted-foreground">Output:</span>
                                            <span className="text-green-600 dark:text-green-400">{testCase.output}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="h-2/5 flex flex-col shadow-sm border-t-4 border-t-slate-500">
                    <CardHeader className="py-3 border-b bg-muted/30">
                        <CardTitle className="text-sm font-medium flex items-center gap-2">
                            <Terminal className="h-4 w-4" />
                            Console & Analysis
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 overflow-auto bg-slate-950 text-slate-50 font-mono text-xs relative">
                        {analysis ? (
                            <div className="p-4 space-y-4">
                                <div className="flex items-center gap-2 text-lg font-bold">
                                    {analysis.correctness === "Passed" ? (
                                        <span className="text-green-400 flex items-center gap-2"><CheckCircle className="h-5 w-5" /> Passed</span>
                                    ) : (
                                        <span className="text-red-400 flex items-center gap-2"><XCircle className="h-5 w-5" /> Failed</span>
                                    )}
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-slate-900 p-3 rounded border border-slate-800">
                                        <span className="text-slate-400 block mb-1">Time Complexity</span>
                                        <span className="text-blue-300">{analysis.time_complexity}</span>
                                    </div>
                                    <div className="bg-slate-900 p-3 rounded border border-slate-800">
                                        <span className="text-slate-400 block mb-1">Space Complexity</span>
                                        <span className="text-purple-300">{analysis.space_complexity}</span>
                                    </div>
                                </div>

                                <div className="bg-slate-900 p-3 rounded border border-slate-800">
                                    <span className="text-slate-400 block mb-1">Feedback</span>
                                    <p className="text-slate-300 leading-relaxed">{analysis.feedback}</p>
                                </div>

                                <div>
                                    <span className="text-slate-400 block mb-1">Raw Output:</span>
                                    <pre className="text-slate-500 whitespace-pre-wrap">{output}</pre>
                                </div>
                            </div>
                        ) : (
                            <pre className="p-4 h-full w-full whitespace-pre-wrap text-slate-300">
                                {output || "> Ready to run..."}
                            </pre>
                        )}
                    </CardContent>
                </Card>
            </div>

            {/* Right Panel: Code Editor */}
            <div className="flex flex-col space-y-4 h-full">
                <Card className="flex-1 flex flex-col overflow-hidden border-0 shadow-lg ring-1 ring-border">
                    <div className="p-2 border-b bg-muted/30 flex justify-between items-center">
                        <div className="w-40">
                            <Select value={language} onValueChange={handleLanguageChange}>
                                <SelectTrigger className="h-8 bg-background">
                                    <SelectValue placeholder="Language" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="python">Python</SelectItem>
                                    <SelectItem value="java">Java</SelectItem>
                                    <SelectItem value="cpp">C++</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex gap-2">
                            <Button
                                variant="secondary"
                                size="sm"
                                onClick={handleRun}
                                disabled={running}
                                className="h-8"
                            >
                                {running ? <Loader2 className="mr-2 h-3 w-3 animate-spin" /> : <Play className="mr-2 h-3 w-3" />}
                                Run Code
                            </Button>
                            <Button
                                size="sm"
                                onClick={handleSubmit}
                                disabled={submitting}
                                className="h-8"
                            >
                                {submitting ? <Loader2 className="mr-2 h-3 w-3 animate-spin" /> : <Send className="mr-2 h-3 w-3" />}
                                Submit
                            </Button>
                        </div>
                    </div>
                    <div className="flex-1 relative">
                        <Editor
                            height="100%"
                            language={language === 'cpp' ? 'cpp' : language}
                            theme="vs-dark"
                            value={code}
                            onChange={(value) => setCode(value || "")}
                            options={{
                                minimap: { enabled: false },
                                fontSize: 14,
                                scrollBeyondLastLine: false,
                                automaticLayout: true,
                                padding: { top: 16, bottom: 16 },
                                fontLigatures: true
                            }}
                        />
                    </div>
                </Card>
            </div>
        </div>
    )
}
